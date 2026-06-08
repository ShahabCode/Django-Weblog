# 📝 Django Weblog

A backend-focused weblog application built with **Django** and **PostgreSQL**.

This project demonstrates authentication, content management, image handling, PostgreSQL-powered search, user profiles, and custom Django features commonly used in real-world applications.

---

## 🚀 Features

| Feature | Description |
|----------|-------------|
| 🔐 Authentication | User registration, login, logout and profile management |
| 📝 Post Management | Create, edit and delete blog posts |
| 🖼️ Image Handling | Multiple images per post with automatic resizing |
| 🗑️ Media Cleanup | Automatic deletion of unused uploaded files |
| 💬 Comments | Comment system with moderation support |
| 🔍 Search | PostgreSQL TrigramSimilarity-based search |
| 📂 Categories | Filter posts by category |
| 📄 Pagination | Efficient post listing |
| 📊 Custom Template Tags | Blog statistics and latest posts |
| ✍️ Markdown Support | Render Markdown content |
| 📅 Jalali Dates | Persian date support using django-jalali |

---

## 🛠️ Tech Stack

| Layer | Technology |
|--------|------------|
| Backend | Django 6 |
| Database | PostgreSQL |
| Authentication | Django Auth |
| Search | PostgreSQL Trigram Search |
| Media Processing | django-resized |
| Date System | django-jalali |

---

## 📁 Project Structure

```text
Django-Weblog/
├── Weblog/             # Project settings
├── blog/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── templatetags/
│   ├── models.py
│   ├── views.py
│   └── forms.py
├── images/
│   ├── account_images/
│   └── post_images/
├── blog_data.json
├── requirements.txt
└── manage.py
```

---

## ⚙️ Installation

```bash
git clone https://github.com/ShahabCode/Django-Weblog.git

cd Django-Weblog

pip install -r requirements.txt

python manage.py migrate

python manage.py loaddata blog_data.json

python manage.py createsuperuser

python manage.py runserver
```

---

## 🔍 Backend Highlights

- Custom model manager (`PublishedManager`)
- PostgreSQL similarity search (`TrigramSimilarity`)
- Custom template tags and filters
- Automatic slug generation
- Image optimization and resizing
- Media cleanup using Django signals
- Form validation with custom clean methods
- User profile management with OneToOne relationships

---

## 📚 Sample Data

The repository includes:

- `blog_data.json` fixture data
- Sample blog posts
- User profiles
- Media files for posts and accounts

Load the sample data with:

```bash
python manage.py loaddata blog_data.json
```
---

## 🤝 Contributing

Feedback, suggestions, and contributions are always appreciated. Feel free to open an issue or submit a pull request.
