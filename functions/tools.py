from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
import sqlite3


db = sqlite3.connect("database/data.db", check_same_thread=False)
cursor = db.cursor()


@tool
def bank_balance_check(user_id, account_number: int, balance: float) -> bool:
    """
    Check if the bank balance is sufficient for specified account number
    """
    cursor.execute(
        f"SELECT balance FROM users WHERE account_number = {account_number} AND userid = {user_id}"
    )
    result = cursor.fetchone()
    if result:
        return float(balance) <= float(result[0])
    return False


@tool
def transfer_funds(user_id, from_account: int, to_account: int, amount: float) -> bool:
    """
    Transfer funds from one account to another
    """
    cursor.execute(
        f"SELECT balance FROM users WHERE account_number = {from_account} AND userid = {user_id}"
    )
    result = cursor.fetchone()
    if result and float(result[0]) >= float(amount):
        cursor.execute(
            f"UPDATE users SET balance = balance - {amount} WHERE account_number = {from_account}"
        )
        cursor.execute(
            f"UPDATE users SET balance = balance + {amount} WHERE account_number = {to_account}"
        )
        db.commit()
        return True
    return False


transfer_funds_tools = [bank_balance_check, transfer_funds]
transfer_funds_tool_node = ToolNode(transfer_funds_tools)


@tool
def password_change_tool(user_id, old_password: str, new_password: str) -> bool:
    """
    Change the password of the user
    """
    cursor.execute(f"SELECT password FROM users WHERE userid = {user_id}")
    result = cursor.fetchone()
    if result and result[0] == old_password:
        cursor.execute(
            f"UPDATE users SET password = '{new_password}' WHERE userid = {user_id}"
        )
        db.commit()
        return True
    return False


SEARCH_TOOL = TavilySearchResults(max_results=2)
