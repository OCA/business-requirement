# -*- coding: utf-8 -*-
def migrate(cr, version):
    cr.execute("""UPDATE business_requirement
               SET responsible_id = create_uid
            """)
