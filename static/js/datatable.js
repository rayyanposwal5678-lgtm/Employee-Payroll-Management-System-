/**
 * EPMS — Premium DataTable Engine v1.0
 * Auto-enhances tables with class "epms-datatable".
 * Features: Search, column sorting, pagination, row count, zebra striping.
 * Zero dependencies — pure vanilla JavaScript.
 */

(function () {
    'use strict';

    const ROWS_PER_PAGE = 25;

    document.addEventListener('DOMContentLoaded', function () {
        const tables = document.querySelectorAll('.epms-datatable');
        tables.forEach(table => new EPMSDataTable(table));
    });

    function EPMSDataTable(table) {
        this.table = table;
        this.thead = table.querySelector('thead');
        this.tbody = table.querySelector('tbody');
        if (!this.thead || !this.tbody) return;

        this.allRows = Array.from(this.tbody.querySelectorAll('tr'));
        this.filteredRows = [...this.allRows];
        this.currentPage = 1;
        this.sortCol = -1;
        this.sortAsc = true;

        this.init();
    }

    EPMSDataTable.prototype.init = function () {
        this.buildToolbar();
        this.buildSortHeaders();
        this.buildPagination();
        this.render();
    };

    // ── Toolbar: Search + Row Count ──────────────────────
    EPMSDataTable.prototype.buildToolbar = function () {
        const wrapper = this.table.closest('.table-responsive') || this.table.parentElement;
        const toolbar = document.createElement('div');
        toolbar.className = 'dt-toolbar';
        toolbar.innerHTML = `
            <div class="dt-toolbar-left">
                <div class="input-icon-wrap">
                    <i class="fas fa-search input-icon"></i>
                    <input type="text" class="form-control dt-search" placeholder="Search this table..." />
                </div>
            </div>
            <div class="dt-toolbar-right">
                <span class="dt-row-count"></span>
            </div>
        `;
        wrapper.parentElement.insertBefore(toolbar, wrapper);

        const searchInput = toolbar.querySelector('.dt-search');
        this.rowCountEl = toolbar.querySelector('.dt-row-count');

        let debounce;
        searchInput.addEventListener('input', () => {
            clearTimeout(debounce);
            debounce = setTimeout(() => {
                this.filterRows(searchInput.value.toLowerCase().trim());
            }, 150);
        });
    };

    // ── Sort Headers ─────────────────────────────────────
    EPMSDataTable.prototype.buildSortHeaders = function () {
        const ths = this.thead.querySelectorAll('th');
        const self = this;
        ths.forEach((th, index) => {
            // Skip "Actions" column
            if (th.textContent.trim().toLowerCase() === 'actions') return;

            th.classList.add('dt-sortable');
            const icon = document.createElement('span');
            icon.className = 'dt-sort-icon';
            icon.innerHTML = '<i class="fas fa-sort"></i>';
            th.appendChild(icon);

            th.addEventListener('click', function () {
                // Reset all icons
                ths.forEach(h => {
                    const ic = h.querySelector('.dt-sort-icon i');
                    if (ic) ic.className = 'fas fa-sort';
                    h.classList.remove('dt-sorted-asc', 'dt-sorted-desc');
                });

                if (self.sortCol === index) {
                    self.sortAsc = !self.sortAsc;
                } else {
                    self.sortCol = index;
                    self.sortAsc = true;
                }

                const myIcon = icon.querySelector('i');
                myIcon.className = self.sortAsc ? 'fas fa-sort-up' : 'fas fa-sort-down';
                th.classList.add(self.sortAsc ? 'dt-sorted-asc' : 'dt-sorted-desc');

                self.sortRows();
            });
        });
    };

    // ── Sort Logic ───────────────────────────────────────
    EPMSDataTable.prototype.sortRows = function () {
        const col = this.sortCol;
        const asc = this.sortAsc;

        this.filteredRows.sort(function (a, b) {
            const aText = (a.cells[col]?.textContent || '').trim();
            const bText = (b.cells[col]?.textContent || '').trim();

            // Try numeric comparison first (strip $ , # + -)
            const aNum = parseFloat(aText.replace(/[$,#\+\-\s]/g, ''));
            const bNum = parseFloat(bText.replace(/[$,#\+\-\s]/g, ''));

            if (!isNaN(aNum) && !isNaN(bNum)) {
                return asc ? aNum - bNum : bNum - aNum;
            }

            // String comparison
            return asc
                ? aText.localeCompare(bText, undefined, { numeric: true })
                : bText.localeCompare(aText, undefined, { numeric: true });
        });

        this.currentPage = 1;
        this.render();
    };

    // ── Filter (Search) ──────────────────────────────────
    EPMSDataTable.prototype.filterRows = function (query) {
        if (!query) {
            this.filteredRows = [...this.allRows];
        } else {
            this.filteredRows = this.allRows.filter(row => {
                return row.textContent.toLowerCase().includes(query);
            });
        }
        this.currentPage = 1;
        this.render();
    };

    // ── Pagination Controls ──────────────────────────────
    EPMSDataTable.prototype.buildPagination = function () {
        const wrapper = this.table.closest('.table-responsive') || this.table.parentElement;
        this.paginationEl = document.createElement('div');
        this.paginationEl.className = 'dt-pagination';
        // Insert after the table wrapper
        wrapper.parentElement.insertBefore(this.paginationEl, wrapper.nextSibling);
    };

    EPMSDataTable.prototype.render = function () {
        const total = this.filteredRows.length;
        const totalPages = Math.max(1, Math.ceil(total / ROWS_PER_PAGE));
        if (this.currentPage > totalPages) this.currentPage = totalPages;

        const start = (this.currentPage - 1) * ROWS_PER_PAGE;
        const end = start + ROWS_PER_PAGE;

        // Update row count text
        if (this.rowCountEl) {
            if (total === 0) {
                this.rowCountEl.textContent = 'No results';
            } else {
                this.rowCountEl.textContent = `Showing ${start + 1}–${Math.min(end, total)} of ${total}`;
            }
        }

        // Identify columns to highlight (based on header text)
        const ths = Array.from(this.thead.querySelectorAll('th'));
        const nameCols = [];
        const amountCols = [];

        ths.forEach((th, idx) => {
            const text = th.textContent.trim().toLowerCase();
            if (text.includes('name') || text.includes('employee')) {
                nameCols.push(idx);
            }
            if (text.includes('amount') || text.includes('salary') || text.includes('bonus') || 
                text.includes('deduction') || text.includes('net') || text.includes('total') || text.includes('basic')) {
                amountCols.push(idx);
            }
        });

        // Show/hide rows and apply formatting
        this.allRows.forEach(row => row.style.display = 'none');
        this.filteredRows.slice(start, end).forEach((row, idx) => {
            row.style.display = '';
            row.classList.toggle('dt-zebra', idx % 2 === 1);
            
            // Apply column-specific highlights
            Array.from(row.cells).forEach((cell, cellIdx) => {
                if (nameCols.includes(cellIdx)) {
                    cell.classList.add('col-highlight-name');
                } else if (amountCols.includes(cellIdx)) {
                    cell.classList.add('col-highlight-amount');
                }
            });
        });

        // Render pagination buttons
        this.renderPaginationButtons(totalPages);
    };

    EPMSDataTable.prototype.renderPaginationButtons = function (totalPages) {
        if (!this.paginationEl) return;
        this.paginationEl.innerHTML = '';

        if (totalPages <= 1) return;

        const self = this;

        // Previous
        const prevBtn = createPagBtn('‹', this.currentPage > 1, function () {
            self.currentPage--;
            self.render();
        });
        prevBtn.classList.add('dt-page-prev');
        this.paginationEl.appendChild(prevBtn);

        // Page numbers (show max 5 pages centered)
        let startPage = Math.max(1, this.currentPage - 2);
        let endPage = Math.min(totalPages, startPage + 4);
        if (endPage - startPage < 4) startPage = Math.max(1, endPage - 4);

        for (let i = startPage; i <= endPage; i++) {
            const btn = createPagBtn(i, true, function () {
                self.currentPage = i;
                self.render();
            });
            if (i === this.currentPage) btn.classList.add('active');
            this.paginationEl.appendChild(btn);
        }

        // Next
        const nextBtn = createPagBtn('›', this.currentPage < totalPages, function () {
            self.currentPage++;
            self.render();
        });
        nextBtn.classList.add('dt-page-next');
        this.paginationEl.appendChild(nextBtn);
    };

    function createPagBtn(text, enabled, onClick) {
        const btn = document.createElement('button');
        btn.className = 'dt-page-btn';
        btn.textContent = text;
        btn.disabled = !enabled;
        if (enabled) btn.addEventListener('click', onClick);
        return btn;
    }
})();
