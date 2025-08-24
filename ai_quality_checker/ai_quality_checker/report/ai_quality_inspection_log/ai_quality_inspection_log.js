// Copyright (c) 2024, Your Name and contributors
// For license information, please see license.txt

frappe.query_reports["AI Quality Inspection Log"] = {
    "filters": [
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nPending\nPass\nFail"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        }
    ],
    
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        
        if (column.fieldname == "status") {
            if (value === "Pass") {
                value = "<span style='color: green; font-weight: bold;'>" + value + "</span>";
            } else if (value === "Fail") {
                value = "<span style='color: red; font-weight: bold;'>" + value + "</span>";
            } else if (value === "Pending") {
                value = "<span style='color: orange; font-weight: bold;'>" + value + "</span>";
            }
        }
        
        if (column.fieldname == "ai_confidence_score" && value) {
            const score = parseFloat(value);
            let color = "black";
            if (score >= 0.8) {
                color = "green";
            } else if (score >= 0.6) {
                color = "orange";
            } else {
                color = "red";
            }
            value = "<span style='color: " + color + "; font-weight: bold;'>" + score.toFixed(2) + "</span>";
        }
        
        return value;
    }
};
