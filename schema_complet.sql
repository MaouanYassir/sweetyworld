CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "accounts_shopper" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "email" varchar(254) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "accounts_shopper_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "shopper_id" bigint NOT NULL REFERENCES "accounts_shopper" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "accounts_shopper_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "shopper_id" bigint NOT NULL REFERENCES "accounts_shopper" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "accounts_shopper_groups_shopper_id_group_id_81387419_uniq" ON "accounts_shopper_groups" ("shopper_id", "group_id");
CREATE INDEX "accounts_shopper_groups_shopper_id_b0fc95fd" ON "accounts_shopper_groups" ("shopper_id");
CREATE INDEX "accounts_shopper_groups_group_id_e3f091d4" ON "accounts_shopper_groups" ("group_id");
CREATE UNIQUE INDEX "accounts_shopper_user_permissions_shopper_id_permission_id_53b66cc3_uniq" ON "accounts_shopper_user_permissions" ("shopper_id", "permission_id");
CREATE INDEX "accounts_shopper_user_permissions_shopper_id_1f93d8af" ON "accounts_shopper_user_permissions" ("shopper_id");
CREATE INDEX "accounts_shopper_user_permissions_permission_id_0d51f125" ON "accounts_shopper_user_permissions" ("permission_id");
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_shopper" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE TABLE IF NOT EXISTS "shop_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_date" datetime NOT NULL, "update_date" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "accounts_shopper" ("id") DEFERRABLE INITIALLY DEFERRED, "pick_up_date" datetime NULL);
CREATE TABLE IF NOT EXISTS "shop_cartitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "cart_id" bigint NULL REFERENCES "shop_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "shop_product" ("id") DEFERRABLE INITIALLY DEFERRED, "order_id" bigint NULL REFERENCES "shop_order" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "shop_cart_user_id_27925ac6" ON "shop_cart" ("user_id");
CREATE INDEX "shop_cartitem_cart_id_6bf1447e" ON "shop_cartitem" ("cart_id");
CREATE INDEX "shop_cartitem_product_id_09e4b7dd" ON "shop_cartitem" ("product_id");
CREATE INDEX "shop_cartitem_order_id_09ee1b9d" ON "shop_cartitem" ("order_id");
CREATE TABLE IF NOT EXISTS "shop_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "order_date" datetime NOT NULL, "pick_up_date" datetime NULL, "total_price" decimal NULL, "cart_id" bigint NULL REFERENCES "shop_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_shopper" ("id") DEFERRABLE INITIALLY DEFERRED, "is_paid" bool NOT NULL);
CREATE INDEX "shop_order_cart_id_5b16e4f1" ON "shop_order" ("cart_id");
CREATE INDEX "shop_order_user_id_00aba627" ON "shop_order" ("user_id");
CREATE TABLE IF NOT EXISTS "shop_contactmessage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(60) NOT NULL, "email" varchar(254) NOT NULL, "subject" varchar(255) NOT NULL, "message" text NOT NULL, "date_sent" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "shop_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(60) NOT NULL, "image" varchar(100) NOT NULL, "price" decimal NOT NULL, "created_date" datetime NOT NULL, "modified_date" datetime NOT NULL, "categories_id" bigint NOT NULL REFERENCES "shop_category" ("id") DEFERRABLE INITIALLY DEFERRED, "description" text NOT NULL, "description_nl" text NOT NULL, "name" varchar(60) NOT NULL, "name_nl" varchar(60) NOT NULL);
CREATE INDEX "shop_product_slug_30bd2d5d" ON "shop_product" ("slug");
CREATE INDEX "shop_product_categories_id_e0b18cd8" ON "shop_product" ("categories_id");
CREATE TABLE IF NOT EXISTS "shop_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(120) NOT NULL, "image" varchar(100) NOT NULL, "created_date" datetime NOT NULL, "modified_date" datetime NOT NULL, "name_nl" varchar(60) NOT NULL, "name" varchar(60) NOT NULL, "description" text NOT NULL, "description_nl" text NOT NULL);
CREATE INDEX "shop_category_slug_4508178e" ON "shop_category" ("slug");
