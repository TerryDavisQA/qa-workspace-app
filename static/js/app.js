// Global state
let checklistData = [];
let currentSection = null;
let currentItem = null;

// DOM Elements
const sidebarNav = document.querySelector('.sidebar-nav');
const checklistItemsContainer = document.getElementById('checklistItems');
const itemTabsContainer = document.getElementById('itemTabs');
const itemTabsList = document.getElementById('itemTabsList');
const sectionTitle = document.getElementById('sectionTitle');
const progressFill = document.getElementById('progressFill');
const completedCount = document.getElementById('completedCount');
const totalCount = document.getElementById('totalCount');
const resetBtn = document.getElementById('resetBtn');
const exportBtn = document.getElementById('exportBtn');
const toast = document.getElementById('toast');

// Initialize app
async function initApp() {
    await loadChecklist();
    attachEventListeners();
    // Select first section by default
    const firstNavBtn = sidebarNav.querySelector('.nav-btn');
    if (firstNavBtn) {
        firstNavBtn.click();
    }
}

// Load checklist data from API
async function loadChecklist() {
    try {
        const response = await fetch('/api/checklist');
        checklistData = await response.json();
    } catch (error) {
        console.error('Error loading checklist:', error);
        showToast('Error loading checklist', 'error');
    }
}

// Attach event listeners
function attachEventListeners() {
    // Navigation buttons
    const navBtns = sidebarNav.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const sectionId = btn.getAttribute('data-section');
            displaySection(sectionId);
        });
    });

    // Reset button
    resetBtn.addEventListener('click', resetChecklist);

    // Export button
    exportBtn.addEventListener('click', exportChecklist);
}

// Display checklist items for a section with tabs
function displaySection(sectionId) {
    const section = checklistData.find(s => s.id === sectionId);
    if (!section) return;

    currentSection = section;
    sectionTitle.textContent = section.name;

    // Show tabs container and populate with items
    itemTabsContainer.style.display = 'block';
    itemTabsList.innerHTML = '';

    section.items.forEach((item, index) => {
        const tab = document.createElement('button');
        tab.className = 'item-tab' + (index === 0 ? ' active' : '');
        // Use tab_name if available, otherwise use task
        tab.textContent = item.tab_name || item.task;
        tab.setAttribute('data-item-id', item.id);
        
        tab.addEventListener('click', () => {
            // Remove active from all tabs
            itemTabsList.querySelectorAll('.item-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Display the selected item
            displayItemDetail(item);
        });

        itemTabsList.appendChild(tab);
    });

    // Display first item by default
    if (section.items.length > 0) {
        displayItemDetail(section.items[0]);
    }

    updateProgressBar();
}

// Display detailed view of a single item
function displayItemDetail(item) {
    currentItem = item;
    checklistItemsContainer.innerHTML = '';

    // Create detail view
    const detailDiv = document.createElement('div');
    detailDiv.className = 'item-detail-view';

    const header = document.createElement('div');
    header.className = 'item-detail-header';

    const title = document.createElement('div');
    title.className = 'item-detail-title';
    title.innerHTML = `<span>${item.task}</span>`;

    const description = document.createElement('div');
    description.className = 'item-detail-description';
    description.textContent = item.description || 'No description available';

    const checkbox = document.createElement('div');
    checkbox.className = 'item-detail-checkbox';
    checkbox.innerHTML = `
        <input type="checkbox" class="checkbox" id="mainCheckbox" data-item-id="${item.id}" ${item.completed ? 'checked' : ''}>
        <label for="mainCheckbox">Mark as Completed</label>
    `;

    header.appendChild(title);
    header.appendChild(description);
    header.appendChild(checkbox);

    // Add event listener for checkbox
    const checkboxInput = checkbox.querySelector('.checkbox');
    checkboxInput.addEventListener('change', () => toggleItem(item.id));

    // Content section with details
    const contentDiv = document.createElement('div');
    contentDiv.className = 'item-detail-content';

    if (item.details && item.details.length > 0) {
        const sectionTitle = document.createElement('div');
        sectionTitle.className = 'item-detail-section-title';
        sectionTitle.textContent = 'Key Points';

        const detailsList = document.createElement('ul');
        detailsList.className = 'item-details-list';

        item.details.forEach(detail => {
            const li = document.createElement('li');
            li.textContent = detail;
            detailsList.appendChild(li);
        });

        contentDiv.appendChild(sectionTitle);
        contentDiv.appendChild(detailsList);
    }

    detailDiv.appendChild(header);
    detailDiv.appendChild(contentDiv);
    checklistItemsContainer.appendChild(detailDiv);
}

// Toggle item completion
async function toggleItem(itemId) {
    try {
        const response = await fetch(`/api/item/${itemId}/toggle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.success) {
            // Update local data
            for (let section of checklistData) {
                const item = section.items.find(i => i.id === itemId);
                if (item) {
                    item.completed = data.completed;
                    break;
                }
            }

            // Update UI
            const itemElement = document.querySelector(`[data-item-id="${itemId}"]`).closest('.checklist-item');
            const checkbox = itemElement.querySelector('.checkbox');

            if (data.completed) {
                itemElement.classList.add('completed');
                checkbox.checked = true;
                showToast('✓ Item completed');
            } else {
                itemElement.classList.remove('completed');
                checkbox.checked = false;
                showToast('✗ Item marked incomplete');
            }

            updateProgressBar();
        }
    } catch (error) {
        console.error('Error toggling item:', error);
        showToast('Error updating item', 'error');
    }
}

// Update progress bar
async function updateProgressBar() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();

        completedCount.textContent = stats.completed;
        totalCount.textContent = stats.total;
        progressFill.style.width = stats.percentage + '%';
    } catch (error) {
        console.error('Error updating progress:', error);
    }
}

// Reset all items
async function resetChecklist() {
    if (!confirm('Are you sure you want to reset all checklist items? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.success) {
            // Reload checklist
            await loadChecklist();
            if (currentSection) {
                displaySection(currentSection.id);
            }
            showToast('All items reset');
        }
    } catch (error) {
        console.error('Error resetting checklist:', error);
        showToast('Error resetting checklist', 'error');
    }
}

// Export checklist as JSON
async function exportChecklist() {
    try {
        const response = await fetch('/api/export');
        const data = await response.json();

        // Create and download JSON file
        const jsonString = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `qa-checklist-${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        showToast('Checklist exported successfully');
    } catch (error) {
        console.error('Error exporting checklist:', error);
        showToast('Error exporting checklist', 'error');
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = 'toast show';

    if (type === 'error') {
        toast.style.backgroundColor = '#F44336';
    } else {
        toast.style.backgroundColor = '#4CAF50';
    }

    setTimeout(() => {
        toast.classList.remove('show');
    }, 2500);
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);
