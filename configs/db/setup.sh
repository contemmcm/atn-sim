#!/bin/sh

echo "Updating mysql configs in /etc/mysql/my.cnf."

sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/my.cnf

echo "Creating tables and permissions"
if [ "$#" -eq 2 ]; then

    USER=$1
    PASS=$2

    echo "Database user: $USER"
    echo "Password:      ****"

    mysql -u $USER -p$PASS < db.sql
elif [ "$#" -eq 1 ]; then
    USER=$1

    echo "Database user: $USER"
    echo "Password:      <empty>"
    mysql -u $USER < db.sql
else
    echo "Database user: root"
    echo "Password:      <empty>"
    mysql -u root < db.sql
fi

sudo /etc/init.d/mysql stop
sudo /etc/init.d/mysql start
