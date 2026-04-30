UTF-8 Settings
Vikunja itself is always fully capable of handling utf-8 characters. However, your database might not be. Vikunja itself will work just fine until you want to use non-latin characters in your tasks/projects/etc.
On this page, you will find information about how to fully ensure non-latin characters like aüäß or emojis work with your installation.
PostgreSQL & SQLite#
PostgreSQL and SQLite should handle utf-8 just fine - If you discover any issues nonetheless, please drop us a message.
MySQL#
MySQL is not able to handle utf-8 by default. To fix this, follow the steps below.
To find out if your db supports utf-8, run the following in a shell or similar, assuming the database you’re using for Vikunja is called vikunja
:
SELECT default\_character\_set\_name FROM information\_schema.SCHEMATA WHERE schema\_name = 'vikunja';
This will get you a result like the following:
+----------------------------+
| default\_character\_set\_name |
+----------------------------+
| latin1 |
+----------------------------+
1 row in set (0.001 sec)
The charset latin1
means the db is encoded in the latin1
encoding which does not support utf-8 characters.
(The following guide is based on this thread from stackoverflow)
0. Backup your database#
Before attempting any conversion, please back up your database.
1. Create a pre-conversion script#
Copy the following sql statements in a file called preAlterTables.sql
and replace all occurrences of vikunja
with the name of your database:
use information\_schema;
SELECT concat("ALTER DATABASE `",table\_schema,"` CHARACTER SET = utf8mb4 COLLATE = utf8mb4\_unicode\_ci;") as \_sql
FROM `TABLES` where table\_schema like 'vikunja' and TABLE\_TYPE='BASE TABLE' group by table\_schema;
SELECT concat("ALTER TABLE `",table\_schema,"`.`",table\_name,"` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci;") as \_sql
FROM `TABLES` where table\_schema like 'vikunja' and TABLE\_TYPE='BASE TABLE' group by table\_schema, table\_name;
SELECT concat("ALTER TABLE `",table\_schema,"`.`",table\_name, "` CHANGE `",column\_name,"` `",column\_name,"` ",data\_type,"(",character\_maximum\_length,") CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci",IF(is\_nullable="YES"," NULL"," NOT NULL"),";") as \_sql
FROM `COLUMNS` where table\_schema like 'vikunja' and data\_type in ('varchar','char');
SELECT concat("ALTER TABLE `",table\_schema,"`.`",table\_name, "` CHANGE `",column\_name,"` `",column\_name,"` ",data\_type," CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci",IF(is\_nullable="YES"," NULL"," NOT NULL"),";") as \_sql
FROM `COLUMNS` where table\_schema like 'vikunja' and data\_type in ('text','tinytext','mediumtext','longtext');
2. Run the pre-conversion script#
Running this will create the actual migration script for your particular database structure and save it in a file called alterTables.sql
:
mysql -uroot < preAlterTables.sql | egrep '^ALTER' > alterTables.sql
3. Convert the database#
At this point converting is just a matter of executing the previously generated sql script:
mysql -uroot < alterTables.sql
4. Verify it was successfully converted#
If everything worked as intended, your db collation should now look like this:
SELECT default\_character\_set\_name FROM information\_schema.SCHEMATA WHERE schema\_name = 'vikunja';
Should get you:
+----------------------------+
| default\_character\_set\_name |
+----------------------------+
| utf8mb4 |
+----------------------------+
1 row in set (0.001 sec)
