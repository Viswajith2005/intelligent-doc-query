# 🚀 Postman Testing Guide for Intelligent Document Query API

## 📋 **API Overview**
- **Base URL**: `http://127.0.0.1:8000`
- **Authentication**: Bearer Token
- **Team Token**: `acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a`

---

## 🔧 **Setup Instructions**

### **1. Start Your Application**
```cmd
cd "C:\Users\viswa\OneDrive\Desktop\on going projects\bajaj hackathon\intelligent-doc-query"
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### **2. Open Postman**
- Download Postman if you haven't already
- Create a new collection called "Intelligent Document Query API"

---

## 📡 **API Endpoints to Test**

### **1. Health Check**
**GET** `http://127.0.0.1:8000/api/v1/health`

**Headers:**
```
Content-Type: application/json
```

**Expected Response:**
```json
{
    "status": "healthy",
    "message": "API is running successfully"
}
```

---

### **2. Main Hackathon Endpoint**
**POST** `http://127.0.0.1:8000/api/v1/hackrx/run`

**Headers:**
```
Content-Type: application/json
Accept: application/json
Authorization: Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a
```

**Request Body:**
```json
{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}
```

**Expected Response:**
```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
        "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered.",
        "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy. To be eligible, the female insured person must have been continuously covered for at least 24 months. The benefit is limited to two deliveries or terminations during the policy period.",
        "The policy has a specific waiting period of two (2) years for cataract surgery.",
        "Yes, the policy indemnifies the medical expenses for the organ donor's hospitalization for the purpose of harvesting the organ, provided the organ is for an insured person and the donation complies with the Transplantation of Human Organs Act, 1994.",
        "A No Claim Discount of 5% on the base premium is offered on renewal for a one-year policy term if no claims were made in the preceding year. The maximum aggregate NCD is capped at 5% of the total base premium.",
        "Yes, the policy reimburses expenses for health check-ups at the end of every block of two continuous policy years, provided the policy has been renewed without a break. The amount is subject to the limits specified in the Table of Benefits.",
        "A hospital is defined as an institution with at least 10 inpatient beds (in towns with a population below ten lakhs) or 15 beds (in all other places), with qualified nursing staff and medical practitioners available 24/7, a fully equipped operation theatre, and which maintains daily records of patients.",
        "The policy covers medical expenses for inpatient treatment under Ayurveda, Yoga, Naturopathy, Unani, Siddha, and Homeopathy systems up to the Sum Insured limit, provided the treatment is taken in an AYUSH Hospital.",
        "Yes, for Plan A, the daily room rent is capped at 1% of the Sum Insured, and ICU charges are capped at 2% of the Sum Insured. These limits do not apply if the treatment is for a listed procedure in a Preferred Provider Network (PPN)."
    ]
}
```

---

### **3. Legacy Endpoint (File Upload)**
**POST** `http://127.0.0.1:8000/query/`

**Headers:**
```
Content-Type: multipart/form-data
```

**Body (form-data):**
- **Key**: `file` (Type: File)
  - **Value**: Select a PDF file from your computer
- **Key**: `query` (Type: Text)
  - **Value**: `"Does this policy cover knee surgery?"`

**Expected Response:**
```json
{
    "status": "success",
    "message": "Success",
    "data": {
        "query": "Does this policy cover knee surgery?",
        "answer": "Yes, knee surgery is covered under Section 3.2 of your policy...",
        "evaluation": "Likely Yes",
        "execution_time_seconds": 4.2
    }
}
```

---

### **4. Root Endpoint**
**GET** `http://127.0.0.1:8000/`

**Expected Response:**
```json
{
    "message": "Welcome to Intelligent Document Query API! Visit /docs to try the API."
}
```

---

## 🧪 **Step-by-Step Testing in Postman**

### **Step 1: Test Health Check**
1. Create a new request in Postman
2. Set method to **GET**
3. Enter URL: `http://127.0.0.1:8000/api/v1/health`
4. Click **Send**
5. Verify you get a successful response

### **Step 2: Test Main Hackathon Endpoint**
1. Create a new request in Postman
2. Set method to **POST**
3. Enter URL: `http://127.0.0.1:8000/api/v1/hackrx/run`
4. Go to **Headers** tab and add:
   - `Content-Type`: `application/json`
   - `Accept`: `application/json`
   - `Authorization`: `Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a`
5. Go to **Body** tab
6. Select **raw** and **JSON**
7. Paste the request body from above
8. Click **Send**
9. Verify you get the expected response with 10 answers

### **Step 3: Test File Upload (Optional)**
1. Create a new request in Postman
2. Set method to **POST**
3. Enter URL: `http://127.0.0.1:8000/query/`
4. Go to **Body** tab
5. Select **form-data**
6. Add key `file` (Type: File) and select a PDF
7. Add key `query` (Type: Text) with your question
8. Click **Send**

---

## 🔍 **Testing Scenarios**

### **Scenario 1: Valid Request**
- Use the exact request body provided above
- Should return 10 detailed answers
- Processing time should be reasonable (4-10 seconds)

### **Scenario 2: Invalid Token**
- Change the Authorization header to an invalid token
- Should return 401 Unauthorized error

### **Scenario 3: Invalid Document URL**
- Change the documents URL to an invalid one
- Should return 400 Bad Request error

### **Scenario 4: Empty Questions Array**
- Send an empty questions array
- Should return an empty answers array

---

## 📊 **Expected Performance Metrics**

- **Response Time**: 4-10 seconds for 10 questions
- **Memory Usage**: 200-500MB peak
- **Accuracy**: High precision for insurance-related queries
- **Token Efficiency**: Optimized LLM usage

---

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **Connection Refused**
   - Make sure your FastAPI server is running
   - Check if port 8000 is available

2. **401 Unauthorized**
   - Verify the Bearer token is correct
   - Check the Authorization header format

3. **500 Internal Server Error**
   - Check your Azure OpenAI API keys
   - Verify the .env file is properly configured

4. **400 Bad Request**
   - Verify the JSON format is correct
   - Check if the document URL is accessible

### **Debug Steps:**
1. Check the terminal where your server is running for error logs
2. Verify all environment variables are set
3. Test with a smaller number of questions first
4. Check the Swagger UI at `http://127.0.0.1:8000/docs`

---

## ✅ **Success Criteria**

Your API is working correctly if:
- ✅ Health check returns 200 OK
- ✅ Main endpoint processes all 10 questions successfully
- ✅ Response format matches the expected JSON structure
- ✅ Authentication works with the provided token
- ✅ Processing time is reasonable (under 30 seconds)
- ✅ Answers are relevant and accurate

---

## 🎯 **Hackathon Submission**

Once testing is successful:
1. Your API is ready for submission
2. The endpoint `/api/v1/hackrx/run` matches the requirements
3. Authentication is properly implemented
4. Response format is correct
5. Performance meets the criteria

**Good luck with your hackathon submission! 🚀** 