/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     23.10.2019 23:37:36                          */
/*==============================================================*/


drop index Documentation_PK;

drop table Documentation;

drop index Relationship_2_FK;

drop index Relationship_1_FK;

drop index File_PK;

drop table File;

drop index Relationship_3_FK;

drop index Language_PK;

drop table Language;

drop index User_PK;

drop table "User";

/*==============================================================*/
/* Table: Documentation                                         */
/*==============================================================*/
create table Documentation (
   documentation_id     INT4                 not null,
   documentation_link   VARCHAR(100)         null,
   documentation_actor  VARCHAR(45)          null,
   constraint PK_DOCUMENTATION primary key (documentation_id)
);

/*==============================================================*/
/* Index: Documentation_PK                                      */
/*==============================================================*/
create unique index Documentation_PK on Documentation (
documentation_id
);

/*==============================================================*/
/* Table: File                                                  */
/*==============================================================*/
create table File (
   file_id              INT4                 not null,
   user_id              INT4                 null,
   language_id          INT4                 null,
   file_name            VARCHAR(45)          null,
   file_link            VARCHAR(100)         null,
   constraint PK_FILE primary key (file_id)
);

/*==============================================================*/
/* Index: File_PK                                               */
/*==============================================================*/
create unique index File_PK on File (
file_id
);

/*==============================================================*/
/* Index: Relationship_1_FK                                     */
/*==============================================================*/
create  index Relationship_1_FK on File (
user_id
);

/*==============================================================*/
/* Index: Relationship_2_FK                                     */
/*==============================================================*/
create  index Relationship_2_FK on File (
language_id
);

/*==============================================================*/
/* Table: Language                                              */
/*==============================================================*/
create table Language (
   language_id          INT4                 not null,
   documentation_id     INT4                 null,
   language_name        VARCHAR(45)          null,
   language_version     VARCHAR(20)          null,
   constraint PK_LANGUAGE primary key (language_id)
);

/*==============================================================*/
/* Index: Language_PK                                           */
/*==============================================================*/
create unique index Language_PK on Language (
language_id
);

/*==============================================================*/
/* Index: Relationship_3_FK                                     */
/*==============================================================*/
create  index Relationship_3_FK on Language (
documentation_id
);

/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User" (
   user_id              INT4                 not null,
   user_name            VARCHAR(45)          null,
   user_email           VARCHAR(45)          null,
   created_at           VARCHAR(20)          null,
   constraint PK_USER primary key (user_id)
);

/*==============================================================*/
/* Index: User_PK                                               */
/*==============================================================*/
create unique index User_PK on "User" (
user_id
);

alter table File
   add constraint FK_FILE_RELATIONS_USER foreign key (user_id)
      references "User" (user_id)
      on delete restrict on update restrict;

alter table File
   add constraint FK_FILE_RELATIONS_LANGUAGE foreign key (language_id)
      references Language (language_id)
      on delete restrict on update restrict;

alter table Language
   add constraint FK_LANGUAGE_RELATIONS_DOCUMENT foreign key (documentation_id)
      references Documentation (documentation_id)
      on delete restrict on update restrict;

