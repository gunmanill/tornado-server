
--таблица пользователей для входа в интерфейс
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
	"id" SERIAL PRIMARY KEY,
  	"login" varchar(255) NOT NULL,
  	"password" varchar(255) NOT NULL,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"description" text DEFAULT ''::character varying,
	"interface_access" BOOLEAN NOT NULL DEFAULT FALSE,
	"created" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
	"key" text NOT NULL DEFAULT ''::character varying,
	"node_user_access_list" text NOT NULL DEFAULT ''::character varying,
	"node_sudo_access_list" text NOT NULL DEFAULT ''::character varying,
	"class_user_access_list" text NOT NULL DEFAULT ''::character varying,
	"class_sudo_access_list" text NOT NULL DEFAULT ''::character varying
);

DROP INDEX IF EXISTS user_login_ind;
DROP INDEX IF EXISTS user_is_deleted_ind;
CREATE UNIQUE INDEX user_login_ind ON "user" (login);
CREATE INDEX user_is_deleted_ind ON "user" (is_deleted);

INSERT INTO "user" (login, password, interface_access, description) values ('admin', MD5('#2jb9234)(KSFew@8jncsUDHi712345678'), TRUE, 'root');

--таблица забаненных ip адресов
DROP TABLE IF EXISTS "banned_ip";
CREATE TABLE "banned_ip" (
	"ip" BIGINT NOT NULL,
  	"ip_str" varchar(255) NOT NULL,
  	"attempts" INTEGER NOT NULL DEFAULT 0,
  	"date" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);

DROP INDEX IF EXISTS banned_ip_ip_ind;
CREATE UNIQUE INDEX banned_ip_ip_ind ON "banned_ip" (ip);

--таблица серверов
DROP TABLE IF EXISTS "nodes";
CREATE TABLE "nodes" (
	"id" SERIAL PRIMARY KEY,
	"name" varchar(255) NOT NULL,
	"ip" BIGINT NOT NULL,
	"ip_str" varchar(255) NOT NULL
);

DROP INDEX IF EXISTS nodes_ip_ind;
DROP INDEX IF EXISTS nodes_name_ind;
CREATE UNIQUE INDEX nodes_ip_ind ON "nodes" (ip);
CREATE UNIQUE INDEX nodes_name_ind ON "nodes" (name);

--таблица классов
DROP TABLE IF EXISTS "classes";
CREATE TABLE "classes" (
	"id" SERIAL PRIMARY KEY,
	"name" varchar(255) NOT NULL,
	"list" text NOT NULL DEFAULT ''::character varying
);

DROP INDEX IF EXISTS classes_name_ind;
CREATE UNIQUE INDEX classes_name_ind ON "classes" (name);

--таблица логов
DROP TABLE IF EXISTS "log";
CREATE TABLE "log" (
	"id" SERIAL PRIMARY KEY,
	"time" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
	"object_type"  varchar(255) NOT NULL,
	"object" varchar(255) NOT NULL,
	"action" varchar(255) NOT NULL,
	"old_val" text NOT NULL DEFAULT ''::character varying,
	"new_val" text NOT NULL DEFAULT ''::character varying
);

DROP INDEX IF EXISTS log_time_ind;
CREATE UNIQUE INDEX log_time_ind ON "log" (time);


DROP TABLE IF EXISTS "promises";
DROP TYPE IF EXISTS PROMISE_STATUS;
CREATE TYPE PROMISE_STATUS AS ENUM ('dumped', 'queued', 'error', 'complete', 'edit', 'new');

--таблица promisses

CREATE TABLE "promises" (
	"id" SERIAL PRIMARY KEY,
	"created" timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
	"completed" timestamp DEFAULT NULL,
	"user_id" INTEGER NOT NULL,
	"status"  PROMISE_STATUS NOT NULL DEFAULT 'new',
	"promise" text NOT NULL DEFAULT ''::character varying,
	"error" text NOT NULL DEFAULT ''::character varying
);

--если нужно, в последствии создать еще индексы
DROP INDEX IF EXISTS promises_status_ind;
CREATE INDEX promises_status_ind ON "promises" (status);
INSERT INTO "promises" (user_id) (SELECT id FROM "user");

