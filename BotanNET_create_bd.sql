CREATE TABLE tasks (
    "task_id" serial NOT NULL,
    "task_info" TEXT NOT NULL,
    CONSTRAINT tasks_pk PRIMARY KEY ("task_id")
) WITH (
    OIDS=FALSE
);

CREATE TABLE projects (
    "project_id" serial NOT NULL,
    "project_name" varchar(50) NOT NULL,
    "group_id" integer NOT NULL,
    "project_info" TEXT DEFAULT NULL,
    "deadline" TIMESTAMP DEFAULT NULL,
    CONSTRAINT projects_pk PRIMARY KEY ("project_id")
) WITH (
    OIDS=FALSE
);

CREATE TABLE users (
    "user_id" bigint NOT NULL,
    CONSTRAINT users_pk PRIMARY KEY ("user_id")
) WITH (
    OIDS=FALSE
);

CREATE TABLE groups (
    "group_id" serial NOT NULL,
    "group_name" varchar(50) NOT NULL,
    "group_info" TEXT DEFAULT NULL,
    CONSTRAINT groups_pk PRIMARY KEY ("group_id")
) WITH (
    OIDS=FALSE
);

CREATE TABLE user_groups (
    "group_id" integer NOT NULL,
    "user_id" integer NOT NULL,
    "is_admin" bool NOT NULL
) WITH (
    OIDS=FALSE
);

CREATE TABLE project_tasks (
    "project_id" integer NOT NULL,
    "task_id" integer NOT NULL
) WITH (
    OIDS=FALSE
);

CREATE TABLE user_tasks (
    "user_id" integer NOT NULL,
    "task_id" integer NOT NULL,
    "is_hidden" bool NOT NULL DEFAULT 'false',
    "is_done" bool NOT NULL DEFAULT 'false'
) WITH (
    OIDS=FALSE
);


ALTER TABLE projects ADD CONSTRAINT "projects_fk0" FOREIGN KEY ("group_id") REFERENCES groups("group_id");

ALTER TABLE user_groups ADD CONSTRAINT "user_groups_fk0" FOREIGN KEY ("group_id") REFERENCES groups("group_id");
ALTER TABLE user_groups ADD CONSTRAINT "user_groups_fk1" FOREIGN KEY ("user_id") REFERENCES users("user_id");

ALTER TABLE project_tasks ADD CONSTRAINT "project_tasks_fk0" FOREIGN KEY ("project_id") REFERENCES projects("project_id");
ALTER TABLE project_tasks ADD CONSTRAINT "project_tasks_fk1" FOREIGN KEY ("task_id") REFERENCES tasks("task_id");

ALTER TABLE user_tasks ADD CONSTRAINT "user_tasks_fk0" FOREIGN KEY ("user_id") REFERENCES users("user_id");
ALTER TABLE user_tasks ADD CONSTRAINT "user_tasks_fk1" FOREIGN KEY ("task_id") REFERENCES tasks("task_id");


CREATE INDEX deadline_index ON projects(deadline);
