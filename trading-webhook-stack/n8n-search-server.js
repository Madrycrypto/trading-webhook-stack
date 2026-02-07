/**
 * N8N Workflow Search Server
 * API dla wyszukiwarki workflowów N8N
 */

import express from 'express';
import sqlite3 from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

// Database
const db = new sqlite3(path.join(__dirname, 'n8n_workflows.db'));
const getWorkflows = db.prepare('SELECT * FROM workflows');

// Middleware
app.use(express.json());
app.use(express.static(__dirname));

// API endpoint - get all workflows
app.get('/api/workflows', (req, res) => {
    try {
        const workflows = getWorkflows.all();
        res.json(workflows);
    } catch (error) {
        console.error('Database error:', error);
        res.status(500).json({ error: 'Database error' });
    }
});

// API endpoint - search workflows
app.get('/api/workflows/search', (req, res) => {
    try {
        const { q, category } = req.query;
        let query = 'SELECT * FROM workflows WHERE 1=1';
        const params = [];

        if (q) {
            query += ' AND searchable_text LIKE ?';
            params.push(`%${q}%`);
        }

        if (category) {
            query += ' AND category_pl = ?';
            params.push(category);
        }

        const stmt = db.prepare(query);
        const workflows = stmt.all(...params);
        res.json(workflows);
    } catch (error) {
        console.error('Search error:', error);
        res.status(500).json({ error: 'Search error' });
    }
});

// API endpoint - get workflow by ID
app.get('/api/workflows/:id', (req, res) => {
    try {
        const stmt = db.prepare('SELECT * FROM workflows WHERE id = ?');
        const workflow = stmt.get(req.params.id);
        if (workflow) {
            res.json(workflow);
        } else {
            res.status(404).json({ error: 'Workflow not found' });
        }
    } catch (error) {
        console.error('Get workflow error:', error);
        res.status(500).json({ error: 'Database error' });
    }
});

// Serve the search page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'n8n-search.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 N8N Search Server running on http://localhost:${PORT}`);
    console.log(`📊 Database: n8n_workflows.db (${getWorkflows.all().length} workflows)`);
});
