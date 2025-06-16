# from graph.main_graph import run_graph

# def main():
#     print("🔷 Welcome to the Web Project Idea Assistant!")
#     user_prompt = input("💬 Please enter your project idea or prompt:\n> ")
#     output = run_graph(user_prompt)
#     print("\n--- Thinker Agent Output ---\n")
#     print(output)

# if __name__ == "__main__":
#     main()

from graph.main_graph import run_graph
from chains.scaffolder import build_dir_structure
import asyncio
if __name__ == "__main__":
    
    # user_idea = input("Enter your project idea: ")
    # run_graph(user_idea)
        
    input = """
        ## I. Backend Functionalities

    **A. Core Modules:**

    1.  **User Management Module:**

        *   **Functionality:**
            *   **Registration:**
                *   Seller Registration: Collect necessary seller information (business details, contact info, etc.).  Validation of provided data.
                *   Buyer Registration: Collect necessary buyer information (name, email, address, etc.). Validation of provided data.
                *   Hashing and salting passwords for security.
                *   Email verification (sending a verification link to the registered email).
            *   **Authentication:**
                *   Login: Verify user credentials (email/username and password).
                *   Session Management:  Create and manage user sessions (using JWT or similar).
                *   Logout: Invalidate user session.
            *   **Authorization:**
                *   Role-Based Access Control (RBAC): Define roles (Admin, Seller, Buyer) and their corresponding permissions.
                *   Protect API endpoints based on user roles.
            *   **Profile Management:**
                *   Update Profile: Allow users to update their profile information.
                *   Change Password: Allow users to change their password.
                *   Address Management (for buyers): Add, edit, and delete shipping addresses.
            *   **Account Management:**
                *   Account Deactivation: Allow users to deactivate their accounts.
                *   Password Reset: Implement "Forgot Password" functionality (email verification, password reset token).
        *   **External API:**
            *   Email Service Provider (e.g., SendGrid, Mailgun) for sending verification and password reset emails.
        *   **Database:** Stores user data (roles, permissions, profile information, etc.).

    2.  **Product Catalog Management Module:**

        *   **Functionality:**
            *   **Product Creation (Seller):**
                *   Allow sellers to create new product listings.
                *   Collect product information: name, description, images, price, category, inventory, attributes (e.g., color, size).
                *   Validation of product data.
            *   **Product Update (Seller):**
                *   Allow sellers to update existing product listings.
                *   Maintain product history (versioning or audit logs).
            *   **Product Deletion (Seller/Admin):**
                *   Allow sellers to delete their products (with appropriate confirmation).
                *   Allow admins to delete products (e.g., for policy violations).
            *   **Product Retrieval:**
                *   Get Product Details: Retrieve detailed information for a specific product.
                *   List Products: Retrieve a list of products based on various criteria (e.g., category, search query, seller, price range).
                *   Filtering and Sorting: Implement filtering and sorting options for product lists.
            *   **Category Management (Admin):**
                *   Create, update, and delete product categories.
                *   Hierarchical category structure (parent-child relationships).
        *   **External API:**
            *   Image Storage Service (e.g., AWS S3, Cloudinary) for storing product images.
        *   **Database:** Stores product details, categories, attributes, and relationships.

    3.  **Order Management Module:**

        *   **Functionality:**
            *   **Order Creation (Buyer):**
                *   Create an order from the items in the buyer's shopping cart.
                *   Collect shipping address and payment information.
                *   Calculate order total (including shipping costs and taxes).
            *   **Order Processing (Seller/Admin):**
                *   Update order status (e.g., "Pending," "Processing," "Shipped," "Delivered," "Cancelled").
                *   Generate shipping labels.
                *   Manage inventory levels.
            *   **Order Tracking (Buyer/Seller):**
                *   Provide order tracking information to buyers and sellers.
                *   Integrate with shipping provider APIs for real-time tracking updates.
            *   **Order Cancellation (Buyer/Seller):**
                *   Allow buyers to cancel orders (within a certain timeframe).
                *   Allow sellers to cancel orders (e.g., due to insufficient inventory).
            *   **Order History (Buyer/Seller):**
                *   Allow buyers and sellers to view their order history.
        *   **External API:**
            *   Payment Gateway (e.g., Stripe, PayPal) for processing payments.
            *   Shipping Provider (e.g., UPS, FedEx) for generating shipping labels and tracking orders.
        *   **Database:** Stores order details, order items, shipping information, payment information, and order history.

    4.  **Payment Processing Module:**

        *   **Functionality:**
            *   **Payment Integration:** Integrate with one or more payment gateways.
            *   **Payment Capture:** Capture funds from the buyer's payment method.
            *   **Refund Processing:** Process refunds to buyers.
            *   **Transaction Management:** Record and track all payment transactions.
            *   **Fraud Detection:** Implement fraud detection mechanisms (e.g., address verification, CVV verification).
        *   **External API:**
            *   Payment Gateway (e.g., Stripe, PayPal).
        *   **Database:** Stores payment transaction details and payment method information (securely).

    5.  **Search Module:**

        *   **Functionality:**
            *   **Indexing:** Index product data for fast and efficient searching.
            *   **Search Query Processing:** Process user search queries and return relevant results.
            *   **Fuzzy Search:** Implement fuzzy search to handle typos and misspellings.
            *   **Auto-Suggest:** Provide auto-suggested search terms as the user types.
            *   **Filtering and Sorting:** Allow users to filter and sort search results.
        *   **External API:**
            *   Search Service (e.g., Elasticsearch, Solr).
        *   **Database:** Not directly used; the search service maintains its own index.

    6.  **Recommendation Engine Module:**

        *   **Functionality:**
            *   **Data Collection:** Collect user browsing history, purchase history, and product interaction data.
            *   **Recommendation Algorithm:** Implement a recommendation algorithm (e.g., collaborative filtering, content-based filtering).
            *   **Personalized Recommendations:** Generate personalized product recommendations for each user.
            *   **Recommendation Display:** Display recommendations on product pages, the homepage, and other relevant areas.
        *   **Database:** Stores user browsing history, purchase history, and product interaction data.

    7.  **Seller Management Module:**

        *   **Functionality:**
            *   **Seller Registration & Approval:**  Handle seller registration and the admin approval process.
            *   **Seller Dashboard:** Provide sellers with a dashboard to manage their products, orders, and profile.
            *   **Sales Reporting:** Generate sales reports for sellers.
            *   **Communication Tools:** Provide tools for sellers to communicate with buyers (e.g., messaging system).
            *   **Performance Tracking:** Track seller performance metrics (e.g., sales volume, customer ratings).
        *   **Database:** Stores seller-specific information, sales data, and performance metrics.

    8.  **Admin Management Module:**

        *   **Functionality:**
            *   **User Management:** Manage user accounts (create, update, delete).
            *   **Product Management:**  Manage product listings (approve, reject, edit).
            *   **Category Management:** Manage product categories.
            *   **Order Management:** View and manage all orders.
            *   **Dispute Resolution:**  Handle disputes between buyers and sellers.
            *   **Reporting and Analytics:** Generate reports on platform usage, sales, and other key metrics.
            *   **Platform Configuration:** Configure platform settings (e.g., payment gateway settings, shipping options).
        *   **Database:** Access to all data in the database.

    9.  **Notification Service Module:**

        *   **Functionality:**
            *   **Email Notifications:** Send email notifications for order updates, account activity, promotions, etc.
            *   **Push Notifications:** Send push notifications to mobile devices for order updates, promotions, etc.
            *   **Notification Preferences:** Allow users to manage their notification preferences.
        *   **External API:**
            *   Email Service Provider (e.g., SendGrid, Mailgun).
            *   Push Notification Service (e.g., Firebase Cloud Messaging, APNs).
        *   **Database:** Stores notification preferences.

    **B. API Design:**

    *   Use RESTful API principles.
    *   Implement proper authentication and authorization for all API endpoints.
    *   Use versioning for API changes.
    *   Document the API thoroughly (using tools like Swagger/OpenAPI).

    **C. Technology Stack (Example):**

    *   **Language:** Node.js (with TypeScript)
    *   **Framework:** Express.js
    *   **Database:** PostgreSQL (with an ORM like Sequelize or TypeORM)
    *   **Search Service:** Elasticsearch
    *   **Message Queue:** RabbitMQ or Kafka (for asynchronous tasks)
    *   **Cloud Platform:** AWS (EC2, RDS, S3, etc.)

    ## II. Frontend Functionalities

    **A. Core Components:**

    1.  **User Interface (UI) Components:**

        *   Reusable UI components (buttons, input fields, cards, modals, etc.).
        *   Consistent design language and styling.
        *   Responsive design for different screen sizes.

    2.  **Navigation:**

        *   Intuitive navigation menu.
        *   Breadcrumbs for easy navigation.
        *   Footer with important links and information.

    3.  **Homepage:**

        *   Featured products and categories.
        *   Promotional banners and announcements.
        *   Personalized recommendations.

    4.  **Product Listing Page (PLP):**

        *   Display a list of products with images, descriptions, and prices.
        *   Filtering and sorting options.
        *   Pagination for large product lists.

    5.  **Product Detail Page (PDP):**

        *   Display detailed information about a product.
        *   High-quality product images.
        *   Customer reviews and ratings.
        *   "Add to Cart" button.

    6.  **Shopping Cart:**

        *   Display items in the cart with quantities and prices.
        *   Allow users to update quantities or remove items.
        *   Calculate order total.
        *   "Checkout" button.

    7.  **Checkout Process:**

        *   Shipping address form.
        *   Payment method selection.
        *   Order confirmation page.

    8.  **User Account:**

        *   Login and registration forms.
        *   Profile management (update profile, change password).
        *   Order history.
        *   Address book.

    9.  **Seller Dashboard:**

        *   Product management (create, update, delete).
        *   Order management (view, process).
        *   Sales reporting.
        *   Communication with buyers.

    10. **Admin Dashboard:**

        *   User management.
        *   Product management.
        *   Category management.
        *   Order management.
        *   Reporting and analytics.

    **B. Functionality Breakdown:**

    1.  **User Authentication and Authorization:**

        *   Login:  Handle user login using the backend API. Store authentication tokens securely (e.g., in local storage or cookies).
        *   Registration: Handle user registration using the backend API.
        *   Authorization:  Protect routes and components based on user roles.

    2.  **Product Browsing and Searching:**

        *   Fetch product data from the backend API and display it in a user-friendly format.
        *   Implement search functionality using the backend API.
        *   Implement filtering and sorting options.

    3.  **Shopping Cart Management:**

        *   Manage the shopping cart state (using local storage, cookies, or a state management library like Redux or Zustand).
        *   Allow users to add, update, and remove items from the cart.

    4.  **Checkout Process:**

        *   Collect shipping address and payment information.
        *   Send order data to the backend API.
        *   Display order confirmation.

    5.  **Order Tracking:**

        *   Fetch order tracking information from the backend API and display it to the user.

    6.  **Seller Features:**

        *   Provide sellers with a dashboard to manage their products, orders, and profile.
        *   Implement forms for creating and updating product listings.
        *   Display sales reports.

    7.  **Admin Features:**

        *   Provide admins with a dashboard to manage users, products, categories, and orders.
        *   Implement forms for managing users and products.
        *   Display reporting and analytics data.

    8.  **Notifications:**

        *   Display notifications to users for order updates, account activity, and promotions.

    **C. Technology Stack (Example):**

    *   **Framework:** React (with Next.js or Create React App)
    *   **State Management:** Redux or Zustand
    *   **UI Library:** Material UI, Ant Design, or Chakra UI
    *   **Styling:** CSS Modules, Styled Components, or Tailwind CSS
    *   **API Client:** Axios or Fetch

    **D. Key Considerations:**

    *   **User Experience (UX):** Focus on providing a smooth and intuitive user experience.
    *   **Accessibility:** Ensure the platform is accessible to users with disabilities (following WCAG guidelines).
    *   **Performance:** Optimize the frontend for fast loading times and smooth interactions.
    *   **Security:** Protect against common frontend vulnerabilities (e.g., XSS).

    This detailed breakdown provides a solid foundation for developing your e-commerce platform. Remember to adapt and refine these functionalities based on your specific requirements and priorities. Good luck!
    """
    asyncio.run(build_dir_structure(input)) 