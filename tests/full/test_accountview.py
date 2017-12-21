import nose.tools
import tests.utilities


class TestAccountView:
    @classmethod
    def setup_class(cls):
        cls.utilities = tests.utilities.Utilities('TestAccountView')

        # Ensure we don't already have the account
        cls.utilities.delete_account(
            cls.utilities.test_account_name()
        )

        # Create a admin session
        cls.session_admin = cls.utilities.session_pyramid(
            cls.utilities.test_account_admin_name(),
            cls.utilities.test_account_admin_password()
        )

    @classmethod
    def teardown_class(cls):
        # Clean up our account
        cls.utilities.delete_account(
            cls.utilities.test_account_name()
        )

    def test_create_and_delete_account(self):
        cls = type(self)

        # Create the account
        r = cls.session_admin.post(
            '{}/{}'.format(
                cls.utilities.url_base_pyramid(),
                'accounts'
            ),
            json={
                'account': cls.utilities.test_account_name(),
                'password': cls.utilities.test_account_password()
            }
        )
        nose.tools.assert_equal(r.status_code, 201)

        # Creating it again should fail
        r = cls.session_admin.post(
            '{}/{}'.format(
                cls.utilities.url_base_pyramid(),
                'accounts'
            ),
            json={
                'account': cls.utilities.test_account_name(),
                'password': cls.utilities.test_account_password()
            }
        )
        nose.tools.assert_equal(r.status_code, 409)

        # Test the account exists
        r = cls.session_admin.get(
            '{}/{}'.format(
                cls.utilities.url_base_pyramid(),
                'accounts'
            )
        )
        nose.tools.assert_equal(r.status_code, 200)
        nose.tools.assert_in(cls.utilities.test_account_name(), r.json()['accounts'])

        # Delete the account
        r = cls.session_admin.delete(
            '{}/{}/{}'.format(
                cls.utilities.url_base_pyramid(),
                'account',
                cls.utilities.test_account_name()
            )
        )
        nose.tools.assert_equal(r.status_code, 200)

        # Test that deleting the account again fails
        r = cls.session_admin.delete(
            '{}/{}/{}'.format(
                cls.utilities.url_base_pyramid(),
                'account',
                cls.utilities.test_account_name()
            )
        )
        nose.tools.assert_equal(r.status_code, 404)

        # Test the account is gone
        r = cls.session_admin.get(
            '{}/{}'.format(
                cls.utilities.url_base_pyramid(),
                'accounts'
            )
        )
        nose.tools.assert_equal(r.status_code, 200)
        nose.tools.assert_not_in(cls.utilities.test_account_name(), r.json()['accounts'])
