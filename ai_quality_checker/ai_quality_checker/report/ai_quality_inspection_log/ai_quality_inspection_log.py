# Copyright (c) 2024, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("ID"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Material Quality Inspection",
            "width": 120
        },
        {
            "label": _("Item"),
            "fieldname": "item",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": _("Supplier"),
            "fieldname": "supplier",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 150
        },
        {
            "label": _("Inspection Date"),
            "fieldname": "inspection_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("AI Confidence Score"),
            "fieldname": "ai_confidence_score",
            "fieldtype": "Float",
            "width": 130,
            "precision": 2
        },
        {
            "label": _("AI Remarks"),
            "fieldname": "ai_remarks",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Created On"),
            "fieldname": "creation",
            "fieldtype": "Datetime",
            "width": 150
        }
    ]

def get_data(filters):
    conditions = []
    values = []
    
    if filters.get("supplier"):
        conditions.append("supplier = %s")
        values.append(filters.get("supplier"))
    
    if filters.get("status"):
        conditions.append("status = %s")
        values.append(filters.get("status"))
    
    if filters.get("from_date"):
        conditions.append("inspection_date >= %s")
        values.append(filters.get("from_date"))
    
    if filters.get("to_date"):
        conditions.append("inspection_date <= %s")
        values.append(filters.get("to_date"))
    
    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    
    query = f"""
        SELECT
            name,
            item,
            supplier,
            inspection_date,
            status,
            ai_confidence_score,
            ai_remarks,
            creation
        FROM
            `tabMaterial Quality Inspection`
        {where_clause}
        ORDER BY
            inspection_date DESC, creation DESC
    """
    
    return frappe.db.sql(query, tuple(values), as_dict=True)
