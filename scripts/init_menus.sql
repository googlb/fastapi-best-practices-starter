-- Initialize System Roles
-- Ensure these roles exist or insert them.
INSERT INTO sys_roles (name, code, description, created_at, updated_at)
SELECT 'Administrator', 'admin', 'System Administrator with full access', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_roles WHERE code = 'admin');

INSERT INTO sys_roles (name, code, description, created_at, updated_at)
SELECT 'User', 'user', 'Standard User', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_roles WHERE code = 'user');

-- Initialize System Menus
-- 1. System Management (Directory)
INSERT INTO sys_menus (id, parent_id, title, name, path, component, icon, sort, menu_type, is_visible, is_keep_alive, status, created_at, updated_at) 
SELECT 1, NULL, 'System Management', 'System', '/system', 'Layout', 'Settings', 1, 1, true, true, 1, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_menus WHERE id = 1);

-- 2. User Management
INSERT INTO sys_menus (id, parent_id, title, name, path, component, icon, sort, menu_type, is_visible, is_keep_alive, status, created_at, updated_at)
SELECT 2, 1, 'User Management', 'User', '/system/users', '/system/users/index', 'Users', 1, 2, true, true, 1, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_menus WHERE id = 2);

-- 3. Role Management
INSERT INTO sys_menus (id, parent_id, title, name, path, component, icon, sort, menu_type, is_visible, is_keep_alive, status, created_at, updated_at)
SELECT 3, 1, 'Role Management', 'Role', '/system/roles', '/system/roles/index', 'Key', 2, 2, true, true, 1, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_menus WHERE id = 3);

-- 4. Menu Management
INSERT INTO sys_menus (id, parent_id, title, name, path, component, icon, sort, menu_type, is_visible, is_keep_alive, status, created_at, updated_at)
SELECT 4, 1, 'Menu Management', 'Menu', '/system/menus', '/system/menus/index', 'Menu', 3, 2, true, true, 1, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_menus WHERE id = 4);

-- Role-Menu Associations (Admin gets everything)
-- Clear existing associations for admin for these menus to avoid duplicates if re-run, or just insert ignore.
-- Simple approach:
INSERT INTO sys_role_menus (role_id, menu_id, created_at, updated_at)
SELECT r.id, m.id, NOW(), NOW() FROM sys_roles r, sys_menus m
WHERE r.code = 'admin' AND m.id IN (1, 2, 3, 4)
AND NOT EXISTS (SELECT 1 FROM sys_role_menus rm WHERE rm.role_id = r.id AND rm.menu_id = m.id);
