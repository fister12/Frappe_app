// Copyright (c) 2024, Your Name and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material Quality Inspection', {
    refresh: function(frm) {
        // Add custom button for AI analysis if document is saved and has an image
        if (!frm.is_new() && frm.doc.material_image) {
            frm.add_custom_button(__('Analyze with AI'), function() {
                // Display loading message
                frappe.msgprint(__('Starting AI analysis...'));
                
                // Call the server-side whitelisted function
                frappe.call({
                    method: 'ai_quality_checker.api.analyze_image',
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('AI Analysis Complete: ' + r.message));
                            frm.reload_doc(); // Reload to see the updated fields
                        }
                    },
                    error: function(r) {
                        frappe.msgprint(__('Error during AI analysis: ' + r.message));
                    }
                });
            }, __('Actions'));
        }
        
        // Add indicator based on status
        if (frm.doc.status === 'Pass') {
            frm.dashboard.add_indicator(__('Quality Check Passed'), 'green');
        } else if (frm.doc.status === 'Fail') {
            frm.dashboard.add_indicator(__('Quality Check Failed'), 'red');
        } else {
            frm.dashboard.add_indicator(__('Pending Analysis'), 'orange');
        }
    },
    
    material_image: function(frm) {
        // Reset AI fields when image is changed
        if (frm.doc.material_image) {
            frm.set_value('status', 'Pending');
            frm.set_value('ai_confidence_score', '');
            frm.set_value('ai_remarks', '');
        }
    }
});
