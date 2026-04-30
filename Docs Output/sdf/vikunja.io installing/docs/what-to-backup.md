What to backup
There are two parts you need to back up: The database and attachment files.
Project deletion in Vikunja is permanent and irreversible. There is no trash, recycle bin, or undo for deleted projects. Make sure you have a working backup strategy with appropriate retention periods.
Files#
To back up attachments and other files, it is enough to copy them from the attachments folder to some other place.
Database#
MySQL#
To create a backup from MySQL, use the mysqldump
command:
mysqldump -u  -p -h   > vikunja-backup.sql
You will be prompted for the password of the mysql user.
To restore it, simply pipe it back into the mysql
command:
mysql -u  -p -h   < vikunja-backup.sql
PostgreSQL#
To create a backup from PostgreSQL use the pg\_dump
command:
pg\_dump -U  -h   > vikunja-backup.sql
You might be prompted for the password of the database user.
To restore it, simply pipe it back into the psql
command:
psql -U  -h   < vikunja-backup.sql
For more information, please visit the relevant PostgreSQL documentation.
SQLite#
To back up SQLite databases, it is enough to copy the database file to somewhere else.
