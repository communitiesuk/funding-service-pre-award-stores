import json
import threading

from config.mappings.assessment_mapping_fund_round import fund_round_data_key_mappings
from db.queries import bulk_insert_application_record
from fsd_utils.sqs_scheduler.task_executer_service import TaskExecutorService


class AssessmentTaskExecutorService(TaskExecutorService):
    def message_executor(self, message):
        """Processing the message in a separate worker thread and this will call
        the GOV notify service to send emails :param message Json message."""
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        self.logger.info(f"[{thread_id}] Notification Triggered")
        massage_id = message["sqs"]["MessageId"]
        try:
            application_json = json.loads(message["s3"])
            application_json_list = []
            fund_round_shortname = "".join(application_json["reference"].split("-")[:2])
            # Check if the import config exists for the application
            if fund_round_shortname not in fund_round_data_key_mappings.keys():
                self.logger.info.warning(f"Missing import config for the application: {application_json['reference']}.")
                return message

            application_json_list.append(application_json)
            bulk_insert_application_record(application_json_list, is_json=True)
            self.logger.info(f"{thread_id} Processed the message: {massage_id}")
            return message

        except Exception as e:
            self.logger.error(f"An error occurred while processing the message {massage_id}", e)
