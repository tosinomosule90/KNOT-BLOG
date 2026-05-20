# 🪢 Knot - Modern Social Feeds & Media Sharing Platform

Knot is a clean, responsive, and performance-oriented micro-blogging and social networking application built with Python, Flask, and Bootstrap 5. It features real-time search, robust media uploading capabilities (images and videos), multi-tiered nested components, and interactive user management.

---

##  Features

- **Dynamic Social Feed**: Rich card layouts with smooth hover effects, collapsible comment layers, and interactive liking systems.
- **Rich Media Handling**: Seamless support for inline custom profile pictures, image uploads, and native HTML5 video rendering (16:9 aspect ratios).
- **Intelligent Pagination**: Dynamic tokenized page structures using SQLAlchemy's `iter_pages` to handle massive feeds elegantly while maintaining active search parameters across queries.
- **Interactive Comments Section**: Modern chat-bubble design nested cleanly inside parent posts complete with individual user profile thumbnails.
- **Secure Account Controls**: Comprehensive profile updates featuring drag-and-drop styled photo uploads, secure server-side file management, and real-time frontend file selections.
- **Enterprise-Grade Security**: Strict route authorization via Flask-Login, cross-site request forgery protection (CSRF tokens), and dynamic authorship validation to protect posts from manual URL tampering.

---
## Project Structure

```
app.py               # Application entry point
requirements.txt     # Python dependencies
README.md            # Project documentation
app/
├── __init__.py      # Flask app factory and configuration
├── extension.py     # SQLAlchemy and Flask-Login setup
├── model.py         # WTForms form definitions
├── table.py         # Database models and relationships
├── view.py          # Routes, views, and authentication
├── static/          # CSS, JS, images, uploaded media
└── templates/       # HTML templates for pages and layouts
```
##  Technology Stack

- **Backend Architecture**: Python 3.x, Flask (Microframework)
- **Database Layer**: Flask-SQLAlchemy (ORM), SQLite / PostgreSQL
- **Security & Forms**: Werkzeug (Password Hashing), Flask-WTF / WTForms
- **Frontend Engine**: Jinja2 Templates, Vanilla JavaScript (ES6)
- **UI & Styling**: Bootstrap 5, FontAwesome 5/6, Custom CSS Variables

---

## Requirements

- Python 3.10+ recommended
- `Flask`, `Flask-SQLAlchemy`, `Flask-Login`, `Flask-WTF`, `Flask-Dance`, `Flask-Moment`
- SQLite (bundled with Python)

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   # Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

2. Create a `.env` file in the project root with Google OAuth credentials if you want Google login support:

   ```env
   SECRET_KEY=your-super-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

   If you do not use Google OAuth, the app still supports standard email/password login.

3. Start the app:

   ```bash
   python app.py
   ```

4. Open the app in your browser:

   ```text
   http://localhost:5000
   ```

## Usage

Registration: Register a new user account on the signup landing page or log in instantly using Google OAuth.

Core Dashboard: Create rich text posts with attached images or MP4 videos, read chronological interactions, or toggle real-time query searches.

Engagement: Drop reactions using the interactive asymmetric heart layout, or collapse comment threads to converse using custom chat bubbles.

Profile Hub: Manage usernames, emails, or update credentials. Upload custom profile banners using our modern clickable file field component.

## Security & Performance Notes
Orphan File Prevention: Profile picture swaps automatically clean up old storage values using os.remove() inside the storage handler to avoid disk clutter.

Route Guards: Critical data changes (/update-post/, /update-account) perform continuous identity assertion checks ensuring active sessions strictly match data author records.

## homepage display
<img width="259" height="579" alt="Annotation 2026-05-20 135156" src="https://github.com/user-attachments/assets/5d62addf-fcc5-49e4-b622-0b9d90345ab9" />
## update profile display
<img width="264" height="586" alt="upadate" src="https://github.com/user-attachments/assets/25b00bb9-4f49-4e71-9b63-172436fd43ff" />
## feeds display
<img width="276" height="596" alt="feed" src="https://github.com/user-attachments/assets/bf2a024d-7c8e-402c-9fb6-784fed5bb224" />
## sidebar display
<img width="276" height="598" alt="sidebar" src="https://github.com/user-attachments/assets/cf066e81-4e35-449a-a3e1-97bff9ade6e6" />

- The database is created automatically when you run `app.py`
- Uploaded profile pictures are stored in `app/static/profile_pics/`
- Post images and videos are stored in `app/static/post_images/` and `app/static/post_videos/`
- Session and cookie security settings are configured in `app/__init__.py`

## License

This project is provided as-is for development and learning purposes.
