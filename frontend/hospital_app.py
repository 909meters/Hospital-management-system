import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
import json

# Configuration
API_BASE_URL = "http://127.0.0.1:8000/api"

# Page config
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

def safe_json_parse(response):
    """Safely parse JSON response"""
    if not response:
        return None
    
    try:
        return response.json()
    except ValueError as e:
        st.error(f"❌ Connection Error: Unexpected token '<', received HTML instead of JSON")
        st.error(f"Response content type: {response.headers.get('content-type', 'unknown')}")
        st.error(f"Response status: {response.status_code}")
        return None

def make_api_request(endpoint, method='GET', data=None, auth_required=True):
    """Make API request with proper headers"""
    headers = {'Content-Type': 'application/json'}
    
    if auth_required and st.session_state.token:
        headers['Authorization'] = f'Token {st.session_state.token}'
    
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        # Debug information for errors
        if response.status_code >= 400:
            st.error(f"❌ API Error ({response.status_code}): {url}")
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    error_data = response.json()
                    st.error(f"Error details: {error_data}")
                except:
                    st.error(f"Response: {response.text[:200]}")
            else:
                st.error("❌ Connection Error: Unexpected token '<', received HTML instead of JSON")
                
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Connection Error: {str(e)}")
        return None

def login_page():
    """Login page"""
    st.markdown('<h1 class="main-header">🏥 Hospital Management System</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username and password:
                    # Try to authenticate
                    response = make_api_request('/auth/login/', 'POST', {
                        'username': username,
                        'password': password
                    }, auth_required=False)
                    
                    if response and response.status_code == 200:
                        data = safe_json_parse(response)
                        if data:
                            st.session_state.token = data.get('token')
                            st.session_state.user = data.get('user', {})
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Failed to parse login response.")
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.error("Please enter both username and password.")

def main_dashboard():
    """Main dashboard after login"""
    st.markdown('<h1 class="main-header">🏥 Hospital Management Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.write(f"Welcome, {st.session_state.user.get('first_name', 'User')}!")
        st.write(f"Role: {st.session_state.user.get('role', 'N/A')}")
        
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
        
        st.divider()
        
        # Initialize current page if not set
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard Overview"
        
        page = st.selectbox("Navigate to:", [
            "Dashboard Overview",
            "Patients", 
            "Appointments",
            "Medical Records",
            "Users"
        ], index=0 if st.session_state.current_page == "Dashboard Overview" else 
                  1 if st.session_state.current_page == "Patients" else 
                  2 if st.session_state.current_page == "Appointments" else 
                  3 if st.session_state.current_page == "Medical Records" else 
                  4 if st.session_state.current_page == "Users" else 0)
        
        # Update current page if selection changed
        if page != st.session_state.current_page:
            st.session_state.current_page = page
    
    # Main content based on selected page
    current_page = st.session_state.current_page
    if current_page == "Dashboard Overview":
        dashboard_overview()
    elif current_page == "Patients":
        patients_page()
    elif current_page == "Appointments":
        appointments_page()
    elif current_page == "Medical Records":
        medical_records_page()
    elif current_page == "Users":
        users_page()

def dashboard_overview():
    """Dashboard overview with metrics"""
    st.subheader("📊 Dashboard Overview")
    
    # Get current user info to show personalized dashboard
    user_response = make_api_request('/users/profile/')
    user_role = None
    
    if user_response and user_response.status_code == 200:
        user_data = safe_json_parse(user_response)
        user_role = user_data.get('role') if user_data else None
        
        # Display user info
        st.info(f"Welcome, {user_data.get('first_name', '')} {user_data.get('last_name', '')} ({user_role})")
    
    if user_role == 'PATIENT':
        # Patient dashboard - show only own appointments and records
        st.subheader("📅 My Appointments")
        appointments_response = make_api_request('/scheduling/appointments/')
        
        if appointments_response and appointments_response.status_code == 200:
            appointments_data = safe_json_parse(appointments_response)
            appointments_list = appointments_data.get('results', []) if appointments_data else []
            if appointments_list:
                df = pd.DataFrame(appointments_list)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("You have no appointments.")
        else:
            st.error("Unable to fetch your appointments.")
            
        st.subheader("📋 Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📅 Schedule New Appointment"):
                st.session_state.current_page = "Appointments"
                st.rerun()
        with col2:
            if st.button("📋 View Medical Records"):
                st.session_state.current_page = "Medical Records"
                st.rerun()
                
    else:
        # Doctor/Admin dashboard - show full overview
        patients_response = make_api_request('/patients/')
        appointments_response = make_api_request('/scheduling/appointments/')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if patients_response and patients_response.status_code == 200:
                patients_data = safe_json_parse(patients_response)
                patients_count = len(patients_data.get('results', [])) if patients_data else 0
            else:
                patients_count = 0
            st.metric("Total Patients", patients_count)
        
        with col2:
            if appointments_response and appointments_response.status_code == 200:
                appointments_data = safe_json_parse(appointments_response)
                appointments_count = len(appointments_data.get('results', [])) if appointments_data else 0
            else:
                appointments_count = 0
            st.metric("Total Appointments", appointments_count)
        
        with col3:
            st.metric("Active Users", "TBD")
        
        with col4:
            st.metric("Today's Appointments", "TBD")
        
        # Recent activity
        st.subheader("📅 Recent Appointments")
        if appointments_response and appointments_response.status_code == 200:
            appointments_data = safe_json_parse(appointments_response)
            appointments_list = appointments_data.get('results', []) if appointments_data else []
            if appointments_list:
                df = pd.DataFrame(appointments_list)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No appointments found.")
        else:
            st.error("Unable to fetch appointments data.")

def patients_page():
    """Patients management page"""
    st.subheader("👥 Patients Management")
    
    # Get current user role
    user_role = st.session_state.user.get('role', '')
    
    if user_role == 'PATIENT':
        # For patients, show only their own profile (read-only)
        st.info("As a patient, you can only view your own profile information.")
        
        # Get current user profile
        user_profile_response = make_api_request('/users/profile/')
        if user_profile_response and user_profile_response.status_code == 200:
            user_data = safe_json_parse(user_profile_response)
            user_id = user_data.get('id') if user_data else None
            
            if user_id:
                # Fetch patient profile
                patient_response = make_api_request('/patients/')
                if patient_response and patient_response.status_code == 200:
                    patients_data = safe_json_parse(patient_response)
                    patients_list = patients_data.get('results', []) if patients_data else []
                    
                    if patients_list and len(patients_list) > 0:
                        patient_data = patients_list[0]  # Should only be one patient (current user)
                        
                        st.subheader("Your Profile Information")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Personal Information:**")
                            st.write(f"Name: {patient_data.get('full_name', 'N/A')}")
                            st.write(f"Date of Birth: {patient_data.get('date_of_birth', 'N/A')}")
                            st.write(f"Phone: {patient_data.get('phone_number', 'N/A')}")
                        
                        with col2:
                            st.write("**Contact Information:**")
                            st.write(f"Email: {user_data.get('email', 'N/A')}")
                            st.write(f"Address: {patient_data.get('address', 'N/A')}")
                    else:
                        st.warning("Patient profile not found.")
                else:
                    st.error("Unable to fetch your profile information.")
            else:
                st.error("Unable to get your user information.")
        else:
            st.error("Unable to fetch your profile information.")
            
    else:
        # For doctors/admins, show full patient management functionality
        tab1, tab2 = st.tabs(["View Patients", "Add Patient"])
        
        with tab1:
            # Fetch and display patients
            patients_response = make_api_request('/patients/')
            
            if patients_response and patients_response.status_code == 200:
                patients_data = safe_json_parse(patients_response)
                patients_list = patients_data.get('results', []) if patients_data else []
                
                if patients_list:
                    df = pd.DataFrame(patients_list)
                    
                    # Add search and filter
                    search_term = st.text_input("Search patients by name or phone")
                    if search_term:
                        df = df[df.apply(lambda row: search_term.lower() in 
                                       f"{row.get('first_name', '')} {row.get('last_name', '')} {row.get('phone', '')}".lower(), 
                                       axis=1)]
                    
                    st.dataframe(df, use_container_width=True)
                    
                    # Patient selection for detailed view
                    if len(df) > 0:
                        selected_patient_id = st.selectbox("Select patient for details:", 
                                                         df['user_id'].tolist(), 
                                                         format_func=lambda x: f"{df[df['user_id']==x]['full_name'].iloc[0]}")
                        
                        if st.button("View Patient Details"):
                            patient_detail_response = make_api_request(f'/patients/{selected_patient_id}/')
                            if patient_detail_response and patient_detail_response.status_code == 200:
                                patient_data = safe_json_parse(patient_detail_response)
                                if patient_data:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write("**Personal Information:**")
                                        st.write(f"Name: {patient_data.get('full_name', 'N/A')}")
                                        st.write(f"Date of Birth: {patient_data.get('date_of_birth', 'N/A')}")
                                        st.write(f"Phone: {patient_data.get('phone_number', 'N/A')}")
                                    
                                    with col2:
                                        st.write("**Address:**")
                                        st.write(f"{patient_data.get('address', 'N/A')}")
                                else:
                                    st.error("Failed to parse patient data.")
                            else:
                                st.error("Failed to fetch patient details.")
                else:
                    st.info("No patients found.")
            else:
                st.error("Unable to fetch patients data.")
        
        with tab2:
            # Add new patient form (only for doctors/admins)
            st.subheader("Add New Patient")
            
            with st.form("add_patient_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name*")
                    last_name = st.text_input("Last Name*")
                    date_of_birth = st.date_input("Date of Birth*")
                    phone_number = st.text_input("Phone Number*")
                
                with col2:
                    email = st.text_input("Email")
                    address = st.text_area("Address")
                
                submit_patient = st.form_submit_button("Add Patient")
                
                if submit_patient:
                    if first_name and last_name and date_of_birth and phone_number:
                        patient_data = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'date_of_birth': date_of_birth.isoformat(),
                            'phone_number': phone_number,
                            'email': email or '',
                            'address': address or ''
                        }
                        
                        response = make_api_request('/patients/', 'POST', patient_data)
                        
                        if response and response.status_code == 201:
                            st.success("Patient added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to add patient. Please try again.")
                    else:
                        st.error("Please fill in all required fields.")

def appointments_page():
    """Appointments management page"""
    st.subheader("📅 Appointments Management")
    
    tab1, tab2 = st.tabs(["View Appointments", "Schedule Appointment"])
    
    with tab1:
        # Fetch and display appointments
        appointments_response = make_api_request('/scheduling/appointments/')
        
        if appointments_response and appointments_response.status_code == 200:
            appointments_data = safe_json_parse(appointments_response)
            appointments_list = appointments_data.get('results', []) if appointments_data else []
            
            if appointments_list:
                df = pd.DataFrame(appointments_list)
                
                # Date filter
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("From Date", value=date.today())
                with col2:
                    end_date = st.date_input("To Date", value=date.today())
                
                # Status filter
                status_filter = st.selectbox("Filter by Status", 
                                           ["All", "scheduled", "completed", "cancelled", "no_show"])
                
                # Apply filters (basic implementation)
                filtered_df = df.copy()
                if status_filter != "All":
                    filtered_df = filtered_df[filtered_df['status'] == status_filter]
                
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.info("No appointments found.")
        else:
            st.error("Unable to fetch appointments data.")
    
    with tab2:
        # Schedule new appointment
        st.subheader("Schedule New Appointment")
        
        # Check if current user is a patient
        current_user_response = make_api_request('/users/profile/')
        
        if current_user_response and current_user_response.status_code == 200:
            user_data = safe_json_parse(current_user_response)
            if not user_data or user_data.get('role') != 'PATIENT':
                st.warning("⚠️ Only patients can schedule appointments. Please log in with a patient account.")
                return
            
            # Get doctors only
            doctors_response = make_api_request('/users/doctors/')
            
            if doctors_response and doctors_response.status_code == 200:
                doctors_data = safe_json_parse(doctors_response)
                doctors_list = doctors_data.get('results', []) if doctors_data else []
                
                if doctors_list:
                    with st.form("schedule_appointment_form"):
                        st.info("📝 You are scheduling an appointment for yourself")
                        
                        # Doctor selection
                        doctor_options = {f"Dr. {d['first_name']} {d['last_name']} (ID: {d['id']})": d['id'] 
                                        for d in doctors_list}
                        selected_doctor = st.selectbox("Select Doctor*", list(doctor_options.keys()))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            appointment_date = st.date_input("Appointment Date*")
                            start_time = st.time_input("Start Time*", value=datetime.strptime("09:00", "%H:%M").time())
                        
                        with col2:
                            duration = st.selectbox("Duration (minutes)", [30, 45, 60, 90, 120], index=1)
                            status = st.selectbox("Status", ["SCHEDULED", "COMPLETED", "CANCELLED"])
                        
                        notes = st.text_area("Notes")
                        
                        submit_appointment = st.form_submit_button("Schedule Appointment")
                        
                        if submit_appointment:
                            if selected_doctor and appointment_date and start_time:
                                # Combine date and time for start_time
                                start_datetime = datetime.combine(appointment_date, start_time)
                                # Calculate end_time
                                end_datetime = start_datetime + timedelta(minutes=duration)
                                
                                appointment_data = {
                                    'doctor': doctor_options[selected_doctor],
                                    'start_time': start_datetime.isoformat(),
                                    'end_time': end_datetime.isoformat(),
                                    'status': status,
                                    'notes': notes or ''
                                }
                                
                                response = make_api_request('/scheduling/appointments/', 'POST', appointment_data)
                                
                                if response and response.status_code == 201:
                                    st.success("Appointment scheduled successfully!")
                                    st.rerun()
                                else:
                                    error_data = safe_json_parse(response) if response else {}
                                    error_msg = str(error_data) if error_data else "Unknown error"
                                    st.error(f"Failed to schedule appointment: {error_msg}")
                            else:
                                st.error("Please fill in all required fields.")
                else:
                    st.error("No doctors available. Please contact administration.")
            else:
                st.error("Unable to fetch doctors data.")
        else:
            st.error("Unable to fetch user profile data.")

def medical_records_page():
    """Medical records management page"""
    st.subheader("📋 Medical Records")
    
    # Get current user role
    user_role = st.session_state.user.get('role', '')
    
    if user_role == 'PATIENT':
        # For patients, show only their own medical records
        # Get current user ID
        user_profile_response = make_api_request('/users/profile/')
        if user_profile_response and user_profile_response.status_code == 200:
            user_data = safe_json_parse(user_profile_response)
            user_id = user_data.get('id') if user_data else None
            
            if user_id:
                st.write("Viewing your medical records:")
                
                # Fetch medical records for current patient
                records_response = make_api_request(f'/patients/{user_id}/records/')
                
                if records_response and records_response.status_code == 200:
                    records_data = safe_json_parse(records_response)
                    
                    # Handle paginated response
                    if isinstance(records_data, dict) and 'results' in records_data:
                        records_list = records_data['results']
                    elif isinstance(records_data, list):
                        records_list = records_data
                    else:
                        records_list = []
                    
                    if records_list:
                        st.write(f"Found {len(records_list)} medical records:")
                        
                        for record in records_list:
                            # Ensure record is a dictionary
                            if isinstance(record, dict):
                                visit_date = record.get('visit_date', 'Unknown date')
                                created_by = record.get('created_by_name', 'Unknown doctor')
                                
                                with st.expander(f"Record from {visit_date} by Dr. {created_by}"):
                                    st.write(f"**Diagnosis:** {record.get('diagnosis', 'N/A')}")
                                    st.write(f"**Treatment:** {record.get('treatment', 'N/A')}")
                                    st.write(f"**Notes:** {record.get('notes', 'N/A')}")
                                    st.write(f"**Visit Date:** {visit_date}")
                                    st.write(f"**Record ID:** {record.get('id', 'N/A')}")
                            else:
                                st.error(f"Invalid record format: {record}")
                    else:
                        st.info("You have no medical records yet.")
                else:
                    error_msg = "Unable to fetch medical records."
                    if records_response:
                        error_data = safe_json_parse(records_response)
                        if error_data:
                            error_msg += f" Error: {error_data}"
                    st.error(error_msg)
            else:
                st.error("Unable to get your user information.")
        else:
            st.error("Unable to fetch your profile information.")
    
    else:
        # For doctors/admins, show patient selection and ability to add records
        # Get patients for selection
        patients_response = make_api_request('/patients/')
        
        if patients_response and patients_response.status_code == 200:
            patients_data = safe_json_parse(patients_response)
            patients_list = patients_data.get('results', []) if patients_data else []
            
            if patients_list:
                # Patient selection - используем правильные поля
                patient_options = {f"{p['full_name']} (ID: {p['user_id']})": p['user_id'] 
                                 for p in patients_list}
                selected_patient = st.selectbox("Select Patient to view/add medical records:", 
                                              list(patient_options.keys()))
                
                if selected_patient:
                    patient_id = patient_options[selected_patient]
                    
                    tab1, tab2 = st.tabs(["View Records", "Add Record"])
                    
                    with tab1:
                        # Fetch medical records for selected patient
                        records_response = make_api_request(f'/patients/{patient_id}/records/')
                        
                        if records_response and records_response.status_code == 200:
                            records_data = safe_json_parse(records_response)
                            
                            # Handle paginated response
                            if isinstance(records_data, dict) and 'results' in records_data:
                                records_list = records_data['results']
                            elif isinstance(records_data, list):
                                records_list = records_data
                            else:
                                records_list = []
                            
                            if records_list:
                                st.write(f"Found {len(records_list)} medical records:")
                                
                                for record in records_list:
                                    # Ensure record is a dictionary
                                    if isinstance(record, dict):
                                        visit_date = record.get('visit_date', 'Unknown date')
                                        created_by = record.get('created_by_name', 'Unknown doctor')
                                        
                                        with st.expander(f"Record from {visit_date} by Dr. {created_by}"):
                                            st.write(f"**Diagnosis:** {record.get('diagnosis', 'N/A')}")
                                            st.write(f"**Treatment:** {record.get('treatment', 'N/A')}")
                                            st.write(f"**Notes:** {record.get('notes', 'N/A')}")
                                            st.write(f"**Visit Date:** {visit_date}")
                                            st.write(f"**Record ID:** {record.get('id', 'N/A')}")
                                    else:
                                        st.error(f"Invalid record format: {record}")
                            else:
                                st.info("No medical records found for this patient.")
                        else:
                            error_msg = "Unable to fetch medical records."
                            if records_response:
                                error_data = safe_json_parse(records_response)
                                if error_data:
                                    error_msg += f" Error: {error_data}"
                            st.error(error_msg)
                    
                    with tab2:
                        # Add new medical record
                        st.subheader("Add New Medical Record")
                        
                        with st.form("add_medical_record_form"):
                            diagnosis = st.text_area("Diagnosis*", help="Primary diagnosis for this visit")
                            treatment = st.text_area("Treatment*", help="Treatment plan and procedures")
                            notes = st.text_area("Additional Notes", help="Additional observations or instructions")
                            
                            submit_record = st.form_submit_button("Add Medical Record")
                            
                            if submit_record:
                                if diagnosis and treatment:
                                    record_data = {
                                        'diagnosis': diagnosis,
                                        'treatment': treatment,
                                        'notes': notes or ''
                                    }
                                    
                                    response = make_api_request(f'/patients/{patient_id}/records/', 'POST', record_data)
                                    
                                    if response and response.status_code == 201:
                                        st.success("Medical record added successfully!")
                                        st.rerun()
                                    else:
                                        error_data = safe_json_parse(response) if response else {}
                                        error_msg = str(error_data) if error_data else "Unknown error"
                                        st.error(f"Failed to add medical record: {error_msg}")
                                else:
                                    st.error("Please fill in both Diagnosis and Treatment fields.")
            else:
                st.info("No patients available. Please add patients first.")
        else:
            st.error("Unable to fetch patients data.")

def users_page():
    """Users management page (admin only)"""
    st.subheader("👤 Users Management")
    
    # Check if user has admin privileges
    user_role = st.session_state.user.get('role', '')
    
    if user_role not in ['admin', 'doctor']:
        st.error("Access denied. You don't have permission to view this page.")
        return
    
    tab1, tab2 = st.tabs(["View Users", "Add User"])
    
    with tab1:
        # Fetch and display users
        users_response = make_api_request('/users/doctors/')
        
        if users_response and users_response.status_code == 200:
            users_data = safe_json_parse(users_response)
            users_list = users_data.get('results', []) if users_data else []
            
            if users_list:
                df = pd.DataFrame(users_list)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No users found.")
        else:
            st.error("Unable to fetch users data.")
    
    with tab2:
        # Add new user form (admin only)
        if user_role == 'admin':
            st.subheader("Add New User")
            
            with st.form("add_user_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    username = st.text_input("Username*")
                    first_name = st.text_input("First Name*")
                    last_name = st.text_input("Last Name*")
                    email = st.text_input("Email*")
                
                with col2:
                    password = st.text_input("Password*", type="password")
                    role = st.selectbox("Role*", ["admin", "doctor", "nurse", "receptionist"])
                    department = st.text_input("Department")
                    phone = st.text_input("Phone")
                
                submit_user = st.form_submit_button("Add User")
                
                if submit_user:
                    if username and first_name and last_name and email and password and role:
                        user_data = {
                            'username': username,
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'password': password,
                            'role': role,
                            'department': department,
                            'phone': phone
                        }
                        
                        response = make_api_request('/users/doctors/', 'POST', user_data)
                        
                        if response and response.status_code == 201:
                            st.success("User added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to add user. Please try again.")
                    else:
                        st.error("Please fill in all required fields.")
        else:
            st.info("Only administrators can add new users.")

# Main app logic
def main():
    if st.session_state.token is None:
        login_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
