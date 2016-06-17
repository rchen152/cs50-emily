#!/usr/bin/env python

import MySQLdb

db = MySQLdb.connect('mysql.hcs.harvard.edu', 'cs50-emily', 'u7dfLSpFj0d8', 'cs50-emily')

cursor = db.cursor()

#cursor.execute("CREATE TABLE IF NOT EXISTS `lines` (`id` int(10) unsigned NOT NULL AUTO_INCREMENT, `line` varchar(255) NOT NULL, PRIMARY KEY (`id`), UNIQUE KEY `line` (`line`))")

cursor.execute("DROP TABLE `lines`")
cursor.close()

print 'Content-Type: text/html\n\n'
print 'Success'
