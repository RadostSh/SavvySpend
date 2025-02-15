from django.test import TestCase, Client
from django.contrib.auth.models import User
from tracker.models import Transaction, Category, Budget, SavingGoal, Savings
from datetime import date
from django.urls import reverse

class UserAuthenticationTestCase(TestCase):

    def test_register_user(self):
        """Test register a new user"""
        user = User.objects.create_user(username="testuser", password="password123")
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(user.check_password("password123"))

class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_user_login(self):
        """Test user login"""
        response = self.client.post('/login/', {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, 302)

class TransactionTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.category = Category.objects.create(user=self.user, name="Groceries")
        self.transaction = Transaction.objects.create(
            user=self.user,
            date=date.today(),
            type="income",
            amount=100.00,
            category=self.category,
            description="Salary"
        )

    def test_create_transaction(self):
        """Test add the transaction"""
        transaction = Transaction.objects.create(
            user=self.user,
            date="2025-02-15",
            type="income",
            amount=100.00,
            category=self.category,
            description="Salary"
        )
        self.assertEqual(transaction.amount, 100.00)
        self.assertEqual(transaction.type, "income")
        self.assertEqual(transaction.category.name, "Groceries")

    def test_edit_transaction(self):
        """Test edit transaction"""
        response = self.client.post(reverse("edit_transaction", args=[self.transaction.id]), {
            "date": date.today(),
            "type": "expense",
            "amount": 50.00,
            "category": self.category.id,
            "description": "Groceries Shopping"
        })
        self.transaction.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.transaction.amount, 50.00)
        self.assertEqual(self.transaction.type, "expense")

    def test_delete_transaction(self):
        """Test delete transaction"""
        response = self.client.post(reverse("delete_transaction", args=[self.transaction.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), 0)

class BudgetTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.budget = Budget.objects.create(user=self.user, amount=500, month=2, year=2025)

    def test_budget_creation(self):
        """Check the budget was created correctly"""
        self.assertEqual(self.budget.amount, 500)
        self.assertEqual(self.budget.month, 2)
        self.assertEqual(self.budget.year, 2025)

class SavingGoalTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.saving_goal = SavingGoal.objects.create(
            user=self.user,
            name="New Laptop",
            target_amount=1500,
            current_amount=300,
            deadline="2025-12-01"
        )

    def test_saving_goal_progress(self):
        """Check the progress is calculated correctly"""
        self.assertEqual(self.saving_goal.progress_percentage(), 20.0)

class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.category = Category.objects.create(user=self.user, name="Bills")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Bills")

    def test_delete_category(self):
        response = self.client.post(reverse("delete_category", args=[self.category.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 0)

class SavingsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.savings = Savings.objects.create(user=self.user, amount=250.00)

    def test_savings_creation(self):
        self.assertEqual(self.savings.amount, 250.00)
        self.assertEqual(self.savings.user.username, "testuser")

class BudgetTransactionTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.budget = Budget.objects.create(user=self.user, amount=1000, month=2, year=2025)

    def test_budget_updates_after_transaction(self):
        """Check an expense reduces the budget"""
        Transaction.objects.create(
            user=self.user,
            date=date.today(),
            type="expense",
            amount=200,
            description="Rent"
        )

        updated_budget = Budget.objects.get(id=self.budget.id)
        self.assertEqual(updated_budget.amount, 1000)

class AIAdviceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_ai_advice(self):
        """Test AI tips are generated correctly"""
        response = self.client.post(reverse("generate_financial_advice"), {"query": "Как да спестя повече?"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("financial_advice", response.json())

class CurrencyConversionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_currency_conversion(self):
        """Test currency conversion work correctly"""
        response = self.client.get(reverse("convert_currency"), {"from": "USD", "to": "EUR", "amount": "100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("converted_amount", response.json())
