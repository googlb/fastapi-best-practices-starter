-- Initialize System Roles
INSERT INTO sys_roles (name, code, description, created_at, updated_at)
SELECT '管理员', 'admin', '系统管理员，拥有全部权限', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_roles WHERE code = 'admin');

INSERT INTO sys_roles (name, code, description, created_at, updated_at)
SELECT '普通用户', 'user', '标准用户', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_roles WHERE code = 'user');

-- Initialize System Menus (中文名称)
-- 1. 系统管理 (目录)
INSERT INTO sys_menus (id, parent_id, title, name, path, component, icon, sort, menu_type, is_visible, is_keep_alive, status, created_at, updated_at)
SELECT 1, NULL, '系统管理', 'System', '/system', 'Layout', 'Setting', 1, 1, true, true, 1, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_menus WHERE id = 1);

-- 2. 用户管理
INSERT INTO sys_menus (id, parent_id, title, name, path, component, icon, sort, menu_type, is_visible, is_keep_alive, status, created_at, updated_at)
SELECT 2, 1, '用户管理', 'User', '/system/users', '/system/users/index', 'User', 1, 2, true, true, 1, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_menus WHERE id = 2);

-- 3. 角色管理
INSERT INTO sys_menus (id, parent_id, title, name, path, component, icon, sort, menu_type, is_visible, is_keep_alive, status, created_at, updated_at)
SELECT 3, 1, '角色管理', 'Role', '/system/roles', '/system/roles/index', 'SafetyCertificate', 2, 2, true, true, 1, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_menus WHERE id = 3);

-- 4. 菜单管理
INSERT INTO sys_menus (id, parent_id, title, name, path, component, icon, sort, menu_type, is_visible, is_keep_alive, status, created_at, updated_at)
SELECT 4, 1, '菜单管理', 'Menu', '/system/menus', '/system/menus/index', 'Menu', 3, 2, true, true, 1, NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM sys_menus WHERE id = 4);

-- Role-Menu Associations (管理员拥有所有系统菜单)
INSERT INTO sys_role_menus (role_id, menu_id, created_at, updated_at)
SELECT r.id, m.id, NOW(), NOW()
FROM sys_roles r
CROSS JOIN sys_menus m
WHERE r.code = 'admin'
  AND m.id IN (1, 2, 3, 4)
  AND NOT EXISTS (
    SELECT 1 FROM sys_role_menus rm
    WHERE rm.role_id = r.id AND rm.menu_id = m.id
  );
