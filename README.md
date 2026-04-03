#  Gracie Hospital Management System
**Location:** Hebbal, Mysore, Karnataka - 570017  
**Payment:** Google Pay / UPI (`kanspy@okicici`)  
**Currency:** ₹ Indian Rupees (INR)  
**Framework:** Django 5.1 | Python 3.11+

---

##  What Was Changed (India Localization)

| Area | Before | After |
|------|--------|-------|
| Currency | USD ($) | INR (₹) |
| Payment | Stripe + PayPal | Google Pay / UPI |
| Timezone | Africa/Lagos | Asia/Kolkata (IST) |
| Language | en-us | en-in |
| Branding | DCare Inc. | Gracie Hospital |
| Location | Generic | Hebbal, Mysore, Karnataka |
| Service prices | Generic USD | ₹249–₹499 INR |
| Doctor fields | country | city, state, KMC reg. no. |
| Billing | No UTR field | UTR/transaction ID field |
| Django version | 4.2.2 | 5.1.4 |
| Bootstrap | 5.3.3 | 5.3.3 (updated CDN) |
| Font Awesome | 6.0.0 | 6.5.0 |

---

##  Setup Instructions

### 1. Install Python & create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
Edit `.env` file — your UPI ID is already set:
```
GPAY_UPI_ID=kirancrispy@okicici
GPAY_MERCHANT_NAME=Gracie Hospital Management
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create admin superuser
```bash
python manage.py createsuperuser
```

### 6. Load sample services data
```bash
python manage.py loaddata data.json
```

### 7. Run the server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

##  How Google Pay / UPI Payment Works

1. Patient books appointment → fills details → clicks Continue
2. **Checkout page** shows:
   - Bill summary in ₹ INR (with 5% GST)
   - UPI QR code (scan with any UPI app)
   - "Open Google Pay" deep link button (on Android)
   - UPI ID: `krancripy@okicici`
3. Patient pays via Google Pay / PhonePe / Paytm / BHIM
4. Patient enters the **UTR (Transaction Reference Number)** from their UPI app
5. System confirms and marks appointment as **Scheduled**
6. Email sent to doctor + patient

---

##  Sample Services & Prices (₹ INR)

| Service | Consultation Fee |
|---------|-----------------|
| General Medicine | ₹299 |
| Cardiology | ₹499 |
| Orthopaedics | ₹399 |
| Gynaecology & Obstetrics | ₹449 |
| Paediatrics | ₹249 |
| Dermatology | ₹349 |

---

##  Adding Doctors (via Admin Panel)

1. Go to http://127.0.0.1:8000/admin/
2. Create a User account with type "Doctor"
3. Go to Doctor → Add Doctor
4. Fill: Name, Specialization, Qualifications, KMC Registration No., Mobile
5. Set city = Mysore, state = Karnataka

**Sample Mysore Doctor Names to use:**
- Dr. Suresh Nayak — General Medicine, MBBS MD
- Dr. Kavitha Rangaswamy — Gynaecology, MBBS DGO
- Dr. Ravi Gowda — Cardiology, MBBS MD DM
- Dr. Anitha Krishnamurthy — Paediatrics, MBBS DCH
- Dr. Prashanth Hegde — Orthopaedics, MBBS MS Ortho
- Dr. Deepa Srinivas — Dermatology, MBBS DVD

---

##  Project Structure

```
Gracie-Hospital-Management/
├── base/               # Core app (services, appointments, billing, UPI payment)
├── doctor/             # Doctor app
├── patient/            # Patient app
├── userauths/          # Authentication
├── hms_prj/            # Django settings
├── templates/          # All HTML templates
│   ├── base/           # Public pages + checkout (Google Pay)
│   ├── doctor/         # Doctor dashboard
│   ├── patient/        # Patient dashboard
│   ├── email/          # Email templates (India-branded)
│   └── partials/       # Navbar, footer
├── .env                # Environment variables (UPI ID here)
├── requirements.txt    # Updated Python packages
└── README.md           # This file
```

---

##  Important Notes

- **UPI Payments are manual confirmation** — patient enters UTR after paying.
  For auto-verification, you can later integrate Razorpay (Indian gateway) which supports UPI.
- The QR code uses Google Chart API — works without any API key.
- Phone numbers use +91 India prefix throughout.
- All prices are in ₹ INR with 5% GST included.

---

## 📞 Hospital Contact (Update in base.html)
- **Address:** Hebbal, Mysore - 570017, Karnataka
- **Phone:** +91 98765 43210
- **Email:** info@graciehospital.in
- **Hours:** Mon–Sat 8AM–8PM | Emergency 24×7
# Gracie-Hospital-Management
