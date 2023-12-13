* The widget many2many_checkboxes has a bug that avoids to refresh contents
  when checkboxes are unmarked programatically, so when you remove some
  sections on the sales order creation wizard, they won't be reflected in
  screen.
* Include an event when checking/unchecking deliverable for updating sections
  accordingly.
