# QA Manager Actions & Activity Checklist

A clean, lightweight web application for QA Managers to track and manage their activities and checklist items. Built with Flask, HTML, CSS, and JavaScript.

## Features

- 📋 **10 Pre-built Sections** with all checklist items hard-coded
- ✅ **Interactive Checkboxes** to mark items as completed
- 📊 **Progress Tracking** with real-time completion percentage
- 💾 **In-Memory State** - no database required
- 📤 **JSON Export** - download your checklist status anytime
- 🎨 **Clean UI** - responsive and easy to navigate
- 🚀 **Instant Setup** - no complex configuration needed

## Checklist Sections

1. **Governance & Planning** - QA strategy, roles, timelines, toolset, compliance
2. **Quality Gates** - Requirements, Design, Build, Test Readiness, Release gates
3. **Meetings & Communication** - Milestone meetings, standups, defect triage, planning, retrospectives
4. **Test Planning & Preparation** - Strategy, plan, traceability, test data, environment
5. **Test Execution Oversight** - Monitoring, validation, processes, automation, resourcing
6. **Risk Management** - Risk log, quality impact assessment, escalation, root cause
7. **Reporting & Metrics** - Status reports, defect dashboard, release readiness, coverage
8. **Release Activities** - Exit criteria, acceptance, release approval
9. **Post-Release** - Production testing, defect leakage validation, lessons learned
10. **Continuous Improvement** - Process review, automation strategy, team capability, documentation

## Requirements

- Python 3.7+
- Flask 2.3.3+

## Installation

### 1. Clone or Download the Project

Navigate to the project directory:
```bash
cd qa-workspace-app
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will start on **http://localhost:5000**

Open your browser and navigate to: `http://localhost:5000`

## Usage

### View Checklist
- The app displays all 10 sections in the left sidebar
- Click on any section to view its checklist items
- The first section is automatically selected when the app loads

### Mark Items Complete
- Click the checkbox next to any item to mark it as completed
- Completed items show with a strikethrough and green background
- Progress bar updates in real-time

### Track Progress
- View overall completion percentage in the progress bar
- See completed count vs total items
- Progress updates instantly as you check off items

### Export Checklist
- Click the **"Export JSON"** button to download your checklist status
- File is saved as `qa-checklist-YYYY-MM-DD.json`
- Perfect for archiving or sharing your checklist status

### Reset Checklist
- Click the **"Reset All"** button to uncheck all items
- A confirmation dialog will prevent accidental resets
- Useful for starting a new phase or cycle

## Project Structure

```
qa-workspace-app/
├── app.py                    # Flask application with routes and data
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── templates/
│   └── index.html           # Main HTML template
└── static/
    ├── css/
    │   └── style.css        # Application styling
    └── js/
        └── app.js           # JavaScript for interactivity
```

## Technical Details

### Architecture
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **State Management**: In-memory dictionary (server-side)
- **Data Storage**: Hard-coded checklist structure (no database)

### API Endpoints
- `GET /` - Main page
- `GET /api/checklist` - Get current checklist state
- `POST /api/item/<item_id>/toggle` - Toggle item completion
- `GET /api/stats` - Get progress statistics
- `GET /api/export` - Get complete checklist as JSON
- `POST /api/reset` - Reset all items to incomplete

### Storage
- Checklist items are hard-coded in `app.py`
- Item completion state is stored in server memory
- State persists as long as the Flask app is running
- Restarting the app resets all items to incomplete

## Browser Compatibility

- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Notes

- This is a lightweight application designed for single-user or team use
- State is stored in server memory, not persisted to disk
- Perfect for development, testing, or standalone deployment
- No external dependencies beyond Flask
- Responsive design works on desktop, tablet, and mobile

## Future Enhancement Ideas

- User authentication for multi-user scenarios
- Database persistence (SQLite, PostgreSQL)
- User roles and permissions
- Comments and notes on items
- History/audit trail of changes
- Email notifications
- Print-friendly reports

## Support

If you encounter issues:

1. Ensure Python 3.7+ is installed
2. Verify Flask is properly installed: `pip install -r requirements.txt`
3. Try accessing http://localhost:5000 (not https)
4. Check that port 5000 is not already in use
5. Restart the Flask application

## License

This project is provided as-is for QA team use.

---

**Version**: 1.0  
**Last Updated**: 2026  
**Environment**: Flask Development Server
