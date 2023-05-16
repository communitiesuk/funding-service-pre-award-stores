DO $$
DECLARE r2w2id uuid := 'c603d114-5364-4474-a0c4-c41cbf4d3bbd';
BEGIN
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Top', null, '0');

    INSERT INTO section(round_id, title, weighting, path, title_content_id)
    VALUES(r2w2id, 'Application', null, '0.1', 1);
    INSERT INTO section(round_id, title, weighting, path, title_content_id)
    VALUES(r2w2id, 'Assessment', null, '0.2', 2);

    INSERT INTO section(round_id, title, weighting, path, title_content_id)
    VALUES(r2w2id, 'About your organisation', null, '0.1.10', 4);
    INSERT INTO section(round_id, title, weighting, path, title_content_id)
    VALUES(r2w2id, 'Organisation information', null, '0.1.10.10', 3);
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Applicant information', null, '0.1.10.20');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Strategic case', 30, '0.1.30');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Community use', null, '0.1.30.10');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Community engagement', null, '0.1.30.20');


    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Unscored', null, '0.2.10');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Scored', null, '0.2.20');

    INSERT INTO section(round_id, title, weighting, path, title_content_id)
    VALUES(r2w2id, 'Organisation information', null, '0.2.10.10', 3);
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Applicant information', null, '0.2.10.20');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Project information', null, '0.2.10.30');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Asset information', null, '0.2.10.40');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Business plan', null, '0.2.10.50');

    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Strategic case', 30, '0.2.20.30');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Benefits', null, '0.2.20.30.10');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Engagement', null, '0.2.20.30.20');

    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Engaging the community', null, '0.2.20.30.20.10');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Local support', null, '0.2.20.30.20.20');


    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'General information', null, '0.2.10.10.10');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Activities', null, '0.2.10.10.20');
    INSERT INTO section(round_id, title, weighting, path)
    VALUES(r2w2id, 'Partnerships', null, '0.2.10.10.30');

END $$
