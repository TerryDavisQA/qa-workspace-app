from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json

app = Flask(__name__)

# Hard-coded QA Checklist Data
CHECKLIST_DATA = {
    "sections": [
        {
            "id": "governance",
            "name": "Governance & Planning",
            "icon": "📋",
            "items": [
                {
                    "id": "gov_1",
                    "task": "Define QA strategy",
                    "tab_name": "Strategy",
                    "completed": False,
                    "description": "Establish the overall QA strategy and approach for the project",
                    "details": [
                        "Determine scope of testing (manual, automation, performance, security)",
                        "Define testing timeline and milestones",
                        "Identify key quality metrics and KPIs",
                        "Establish testing approach (risk-based, coverage-based, etc.)",
                        "Document quality standards and acceptance criteria"
                    ]
                },
                {
                    "id": "gov_2",
                    "task": "Identify QA roles & responsibilities",
                    "tab_name": "Resources",
                    "completed": False,
                    "description": "Clearly define QA team members and their roles",
                    "details": [
                        "QA Manager/Lead role and responsibilities",
                        "QA Test Engineers/Analysts assignments",
                        "Automation Engineer responsibilities",
                        "Test Data management ownership",
                        "Escalation paths and RACI matrix"
                    ]
                },
                {
                    "id": "gov_3",
                    "task": "Review project plan for QA timelines",
                    "tab_name": "Planning",
                    "completed": False,
                    "description": "Ensure QA activities are properly scheduled in project timeline",
                    "details": [
                        "Review development sprint schedule",
                        "Identify QA planning phase duration",
                        "Plan test execution windows",
                        "Schedule regression testing phases",
                        "Allow buffer time for issues and re-testing"
                    ]
                },
                {
                    "id": "gov_4",
                    "task": "Confirm toolset availability",
                    "tab_name": "Toolsets",
                    "completed": False,
                    "description": "Verify all required QA tools are available and properly licensed",
                    "details": [
                        "Test management tool (e.g., TestRail, Zephyr)",
                        "Automation testing tools (e.g., Selenium, Cypress)",
                        "Defect tracking system (e.g., Jira, Azure DevOps)",
                        "Performance testing tools",
                        "API testing tools and licenses"
                    ]
                },
                {
                    "id": "gov_5",
                    "task": "Identify compliance requirements",
                    "tab_name": "Compliance",
                    "completed": False,
                    "description": "Determine regulatory and compliance obligations affecting QA",
                    "details": [
                        "Industry compliance standards (HIPAA, GDPR, PCI-DSS, SOC2)",
                        "Internal quality standards and policies",
                        "Security and penetration testing requirements",
                        "Audit and documentation requirements",
                        "Third-party certification needs"
                    ]
                },
            ]
        },
        {
            "id": "quality_gates",
            "name": "Quality Gates",
            "icon": "🚪",
            "items": [
                {"id": "qg_1", "task": "Requirements Gate", "completed": False},
                {"id": "qg_2", "task": "Design Gate", "completed": False},
                {"id": "qg_3", "task": "Build/Code Gate", "completed": False},
                {"id": "qg_4", "task": "Test Readiness Gate", "completed": False},
                {"id": "qg_5", "task": "Release Gate", "completed": False},
            ]
        },
        {
            "id": "meetings",
            "name": "Meetings & Communication",
            "icon": "💬",
            "items": [
                {"id": "meet_1", "task": "Milestone meetings", "completed": False},
                {"id": "meet_2", "task": "Daily stand-ups", "completed": False},
                {"id": "meet_3", "task": "Defect triage", "completed": False},
                {"id": "meet_4", "task": "Test planning sessions", "completed": False},
                {"id": "meet_5", "task": "Retrospectives", "completed": False},
            ]
        },
        {
            "id": "test_planning",
            "name": "Test Planning & Preparation",
            "icon": "📝",
            "items": [
                {"id": "tp_1", "task": "Test Strategy", "completed": False},
                {"id": "tp_2", "task": "Test Plan", "completed": False},
                {"id": "tp_3", "task": "Traceability Matrix", "completed": False},
                {"id": "tp_4", "task": "Test Data Plan", "completed": False},
                {"id": "tp_5", "task": "Environment Readiness Checklist", "completed": False},
            ]
        },
        {
            "id": "test_execution",
            "name": "Test Execution Oversight",
            "icon": "⚙️",
            "items": [
                {"id": "te_1", "task": "Monitor test execution", "completed": False},
                {"id": "te_2", "task": "Validate defect quality", "completed": False},
                {"id": "te_3", "task": "Ensure adherence to processes", "completed": False},
                {"id": "te_4", "task": "Review automation coverage", "completed": False},
                {"id": "te_5", "task": "Manage test resourcing", "completed": False},
            ]
        },
        {
            "id": "risk_management",
            "name": "Risk Management",
            "icon": "⚠️",
            "items": [
                {"id": "rm_1", "task": "Maintain QA risk log", "completed": False},
                {"id": "rm_2", "task": "Assess quality impact of delays", "completed": False},
                {"id": "rm_3", "task": "Escalate high-severity issues", "completed": False},
                {"id": "rm_4", "task": "Root cause analysis", "completed": False},
            ]
        },
        {
            "id": "reporting",
            "name": "Reporting & Metrics",
            "icon": "📊",
            "items": [
                {"id": "rep_1", "task": "QA Status Report", "completed": False},
                {"id": "rep_2", "task": "Defect Dashboard", "completed": False},
                {"id": "rep_3", "task": "Release Readiness Report", "completed": False},
                {"id": "rep_4", "task": "Coverage Summary", "completed": False},
            ]
        },
        {
            "id": "release",
            "name": "Release Activities",
            "icon": "🚀",
            "items": [
                {"id": "rel_1", "task": "Validate exit criteria", "completed": False},
                {"id": "rel_2", "task": "Confirm acceptance", "completed": False},
                {"id": "rel_3", "task": "Approve release", "completed": False},
            ]
        },
        {
            "id": "post_release",
            "name": "Post-Release",
            "icon": "✅",
            "items": [
                {"id": "pr_1", "task": "Support production smoke testing", "completed": False},
                {"id": "pr_2", "task": "Validate defect leakage", "completed": False},
                {"id": "pr_3", "task": "Lessons learned workshop", "completed": False},
            ]
        },
        {
            "id": "continuous_improvement",
            "name": "Continuous Improvement",
            "icon": "🔄",
            "items": [
                {"id": "ci_1", "task": "Review testing processes", "completed": False},
                {"id": "ci_2", "task": "Improve automation strategy", "completed": False},
                {"id": "ci_3", "task": "Assess team capability", "completed": False},
                {"id": "ci_4", "task": "Update documentation", "completed": False},
            ]
        }
    ]
}

# In-memory storage for checklist state
checklist_state = {}

# Initialize checklist state with default values
def initialize_state():
    global checklist_state
    for section in CHECKLIST_DATA["sections"]:
        for item in section["items"]:
            checklist_state[item["id"]] = item["completed"]

initialize_state()


@app.route('/')
def index():
    """Main page - display checklist"""
    return render_template('index.html', sections=CHECKLIST_DATA["sections"])


@app.route('/api/checklist', methods=['GET'])
def get_checklist():
    """API endpoint to get current checklist state"""
    response_data = []
    for section in CHECKLIST_DATA["sections"]:
        section_data = {
            "id": section["id"],
            "name": section["name"],
            "icon": section["icon"],
            "items": []
        }
        for item in section["items"]:
            item_data = {
                "id": item["id"],
                "task": item["task"],
                "completed": checklist_state.get(item["id"], False)
            }
            # Include optional fields if they exist
            if "tab_name" in item:
                item_data["tab_name"] = item["tab_name"]
            if "description" in item:
                item_data["description"] = item["description"]
            if "details" in item:
                item_data["details"] = item["details"]
            
            section_data["items"].append(item_data)
        response_data.append(section_data)
    return jsonify(response_data)


@app.route('/api/item/<item_id>/toggle', methods=['POST'])
def toggle_item(item_id):
    """Toggle the completion status of a checklist item"""
    if item_id in checklist_state:
        checklist_state[item_id] = not checklist_state[item_id]
        return jsonify({
            "success": True,
            "item_id": item_id,
            "completed": checklist_state[item_id]
        })
    return jsonify({"success": False, "error": "Item not found"}), 404


@app.route('/api/export', methods=['GET'])
def export_checklist():
    """Export the current checklist state as JSON"""
    export_data = {
        "export_date": datetime.now().isoformat(),
        "sections": []
    }
    
    for section in CHECKLIST_DATA["sections"]:
        section_data = {
            "name": section["name"],
            "icon": section["icon"],
            "items": []
        }
        for item in section["items"]:
            section_data["items"].append({
                "task": item["task"],
                "completed": checklist_state.get(item["id"], False)
            })
        export_data["sections"].append(section_data)
    
    return jsonify(export_data)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get completion statistics"""
    total_items = sum(len(section["items"]) for section in CHECKLIST_DATA["sections"])
    completed_items = sum(1 for status in checklist_state.values() if status)
    completion_percentage = int((completed_items / total_items * 100)) if total_items > 0 else 0
    
    return jsonify({
        "total": total_items,
        "completed": completed_items,
        "percentage": completion_percentage
    })


@app.route('/api/reset', methods=['POST'])
def reset_checklist():
    """Reset all checklist items to incomplete"""
    global checklist_state
    checklist_state = {}
    for section in CHECKLIST_DATA["sections"]:
        for item in section["items"]:
            checklist_state[item["id"]] = False
    
    return jsonify({
        "success": True,
        "message": "Checklist reset successfully"
    })


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
