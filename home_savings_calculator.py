def calculate_savings():
    '''
    Based on recommended guidelines from Reddit users, the function calculates the following:
    1. Emergency Fund: 3-6 months of living expenses
    2. Home Maintenance Fund: 1-4% of home value per year
    3. Retirement Savings: 10% of annual income

    It also estimates how much money you may want on hand around the time of purchasing a home
    '''
    print("Welcome to the Savings Calculator!")
    
    # Gather user input
    monthly_expenses = float(input("Enter your total monthly living expenses (e.g., mortgage, utilities, groceries): $"))
    home_value = float(input("Enter the value of your home: $"))
    annual_income = float(input("Enter your annual income: $"))
    
    # Calculate recommended savings
    emergency_fund_min = monthly_expenses * 3
    emergency_fund_max = monthly_expenses * 6
    
    home_maintenance_min = home_value * 0.01
    home_maintenance_max = home_value * 0.04
    
    retirement_savings = annual_income * 0.10  # 10% of annual income
    
    # Calculate money needed at purchase
    down_payment = home_value * 0.20
    initial_maintenance = home_value * 0.01  # Assuming 1% of home value for initial maintenance
    total_needed = down_payment + emergency_fund_min + initial_maintenance
    
    # Display results
    print("\nRecommended Savings:")
    print(f"1. Emergency Fund: ${emergency_fund_min:,.2f} - ${emergency_fund_max:,.2f}")
    print(f"2. Home Maintenance Fund: ${home_maintenance_min:,.2f} - ${home_maintenance_max:,.2f} per year")
    print(f"3. Annual Retirement Contribution: ${retirement_savings:,.2f}")
    print(f"\nMoney Needed at Purchase:")
    print(f"- Down Payment (20%): ${down_payment:,.2f}")
    print(f"- Initial Maintenance (1%): ${initial_maintenance:,.2f}")
    print(f"- Emergency Fund (3 months): ${emergency_fund_min:,.2f}")
    print(f"- Total Needed: ${total_needed:,.2f}")

    print("\nConsider additional savings for short-term goals and maintaining a debt cushion.")

if __name__ == "__main__":
    calculate_savings()
