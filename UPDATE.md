# Updating #

Sometimes, the data model has changed in a way that requires manual actions since the migrations are not able to modfiy everything.

## From 6e838ed to 0c3aeef ##

With this commit, not_null constraints are enforced on Foreign-Key relations 

Execute the following SQL statement (to create a Dummy Category that can be used as default foreign key):

```
INSERT INTO `ophasebase_ophasecategory` (`id`, `name`, `description_template`, `lang`, `priority`) VALUES ('1', 'Dummy', '-', 'de', '99');
```

If you don't have database access, you can create the dummy category via admin interface instead.

Now you can apply the migrations staff/0017\_auto\_20170209\_2319 and exam/0004\_auto\_20170209\_2319.

To assign all former staff persons with tutor status to the dummy category, you can optionally run the following SQL query:

```
UPDATE `staff_person` SET `tutor_for_id` = '1' WHERE `staff_person`.`is_tutor` = 1; 
```

Afterwards you will have to check the conditions of StaffFilterGroups manually as all references to Groups are lost.
