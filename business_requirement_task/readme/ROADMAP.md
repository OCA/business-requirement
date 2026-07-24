- Roll up the real hours spent (`effective_hours`) on the linked tasks. That
  field is defined by `hr_timesheet`, so it belongs in a separate glue module
  (e.g. `business_requirement_task_timesheet`) to keep this module free of the
  timesheet dependency.
