
from django.test import TestCase
from django.contrib.auth import get_user_model

from model_mommy import mommy

from rolepermissions.roles import RolesManager, AbstractUserRole
from rolepermissions.models import UserPermission

class RolRole1(AbstractUserRole):
    available_permissions = {
        'permission1': True,
        'permission2': True,
    }

class RolRole2(AbstractUserRole):
    available_permissions = {
        'permission3': True,
        'permission4': False,
    }

class RolRole3(AbstractUserRole):
    role_name = 'new_name'
    available_permissions = {
        'permission5': False,
        'permission6': False,
    }


class AbstractUserRoleTests(TestCase):

    def setUp(self):
        pass

    def test_get_name(self):
        self.assertEquals(RolRole1.get_name(), 'rol_role1')
        self.assertEquals(RolRole2.get_name(), 'rol_role2')
        self.assertEquals(RolRole3.get_name(), 'new_name')

    def test_assign_Role1_default_permissions(self):
        user = mommy.make(get_user_model())

        RolRole1.assign_default_permissions(user)
        permissions = UserPermission.objects.filter(user=user)

        permission_hash = { p.permission_name: p.is_granted for p in permissions }

        self.assertIn('permission1', permission_hash)
        self.assertTrue(permission_hash['permission1'])
        self.assertIn('permission2', permission_hash)
        self.assertTrue(permission_hash['permission2'])
        self.assertEquals(len(permissions), 2)

    def test_assign_Role2_default_permissions(self):
        user = mommy.make(get_user_model())

        RolRole2.assign_default_permissions(user)
        permissions = UserPermission.objects.filter(user=user)

        permission_hash = { p.permission_name: p.is_granted for p in permissions }

        self.assertIn('permission3', permission_hash)
        self.assertTrue(permission_hash['permission3'])
        self.assertIn('permission4', permission_hash)
        self.assertFalse(permission_hash['permission4'])
        self.assertEquals(len(permissions), 2)

    def test_assign_Role3_default_permissions(self):
        user = mommy.make(get_user_model())

        RolRole3.assign_default_permissions(user)
        permissions = UserPermission.objects.filter(user=user)

        permission_hash = { p.permission_name: p.is_granted for p in permissions }

        self.assertIn('permission5', permission_hash)
        self.assertFalse(permission_hash['permission5'])
        self.assertIn('permission6', permission_hash)
        self.assertFalse(permission_hash['permission6'])
        self.assertEquals(len(permissions), 2)

    def test_assign_role_to_user(self):
        user = mommy.make(get_user_model())

        user_role = RolRole1.assign_role_to_user(user)

        self.assertEquals(user_role.role_name, 'rol_role1')

    def test_instanciate_role(self):
        user = mommy.make(get_user_model())

        user_role = RolRole1.assign_role_to_user(user)

        self.assertIsNotNone(user_role.pk)

    def test_change_user_role(self):
        user = mommy.make(get_user_model())

        user_role = RolRole1.assign_role_to_user(user)

        self.assertEquals(user_role.role_name, 'rol_role1')

        user_role = RolRole2.assign_role_to_user(user)

        self.assertEquals(user_role.role_name, 'rol_role2')

    def test_delete_old_permissions_on_role_change(self):
        user = mommy.make(get_user_model())

        RolRole1().assign_role_to_user(user)
        
        permissions = UserPermission.objects.filter(user=user)

        permission_names = [n.permission_name for n in permissions]

        self.assertIn('permission1', permission_names)
        self.assertIn('permission2', permission_names)
        self.assertEquals(len(permissions), 2)

        RolRole2.assign_role_to_user(user)

        permissions = UserPermission.objects.filter(user=user)

        permission_names = [n.permission_name for n in permissions]

        self.assertIn('permission3', permission_names)
        self.assertIn('permission4', permission_names)
        self.assertEquals(len(permissions), 2)


    def test_permission_list(self):
        self.assertIn('permission1', RolRole1.permission_list())
        self.assertIn('permission2', RolRole1.permission_list())

        self.assertIn('permission3', RolRole2.permission_list())
        self.assertIn('permission4', RolRole2.permission_list())


class RolesManagerTests(TestCase):

    def setUp(self):
        pass

    def test_retrieve_role(self):
        self.assertEquals(RolesManager.retrieve_role('rol_role1'), RolRole1)
        self.assertEquals(RolesManager.retrieve_role('rol_role2'), RolRole2)
