CREATE TABLE "Tasks" (
	"task_id" serial NOT NULL,
	"task_info" TEXT NOT NULL,
	CONSTRAINT Tasks_pk PRIMARY KEY ("task_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Projects" (
	"project_id" serial NOT NULL,
	"group_id" integer NOT NULL,
	"project_name" varchar(50) NOT NULL DEFAULT ''default'',
	"project_info" TEXT DEFAULT 'NULL',
	"deadline" TIMESTAMP DEFAULT 'NULL',
	CONSTRAINT Projects_pk PRIMARY KEY ("project_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Users" (
	"user_id" serial NOT NULL,
	"user_name" varchar(50) NOT NULL,
	"deparment" varchar(30) NOT NULL,
	"dorm_number" integer NOT NULL,
	"group_number" integer NOT NULL,
	CONSTRAINT Users_pk PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Groups" (
	"group_id" serial NOT NULL,
	"group_name" varchar(50) NOT NULL,
	"teacher_name" varchar(100),
	CONSTRAINT Groups_pk PRIMARY KEY ("group_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "UserGroups" (
	"group_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"is_admin" bool NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "ProjectTasks" (
	"project_id" integer NOT NULL,
	"task_id" integer NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "UserTasks" (
	"user_id" integer NOT NULL,
	"task_id" integer NOT NULL,
	"is_hidden" bool NOT NULL DEFAULT 'false',
	"is_done" bool NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Comments" (
	"task_id" integer NOT NULL,
	"comment_no" integer NOT NULL,
	"user_id" integer NOT NULL,
	"comment_text" TEXT NOT NULL
) WITH (
  OIDS=FALSE
);




ALTER TABLE "Projects" ADD CONSTRAINT "Projects_fk0" FOREIGN KEY ("group_id") REFERENCES "Groups"("group_id");



ALTER TABLE "UserGroups" ADD CONSTRAINT "UserGroups_fk0" FOREIGN KEY ("group_id") REFERENCES "Groups"("group_id");
ALTER TABLE "UserGroups" ADD CONSTRAINT "UserGroups_fk1" FOREIGN KEY ("user_id") REFERENCES "Users"("user_id");

ALTER TABLE "ProjectTasks" ADD CONSTRAINT "ProjectTasks_fk0" FOREIGN KEY ("project_id") REFERENCES "Projects"("project_id");
ALTER TABLE "ProjectTasks" ADD CONSTRAINT "ProjectTasks_fk1" FOREIGN KEY ("task_id") REFERENCES "Tasks"("task_id");

ALTER TABLE "UserTasks" ADD CONSTRAINT "UserTasks_fk0" FOREIGN KEY ("user_id") REFERENCES "Users"("user_id");
ALTER TABLE "UserTasks" ADD CONSTRAINT "UserTasks_fk1" FOREIGN KEY ("task_id") REFERENCES "Tasks"("task_id");

ALTER TABLE "Comments" ADD CONSTRAINT "Comments_fk0" FOREIGN KEY ("task_id") REFERENCES "Tasks"("task_id");
ALTER TABLE "Comments" ADD CONSTRAINT "Comments_fk1" FOREIGN KEY ("user_id") REFERENCES "Users"("user_id");

