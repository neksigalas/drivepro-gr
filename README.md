# DrivePro GR — Θεωρία Οδήγησης (Κατηγορία Β)

Gamified web app για την προετοιμασία εξέτασης θεωρίας οδήγησης στην Ελλάδα.

## Πώς να το τρέξεις τοπικά
```
cd C:\Users\admin\Desktop\driving-theory-gr
python serve.py            # ή: python -m http.server 8765
```
Άνοιξε: http://localhost:8765

## Τι περιλαμβάνει (ήδη λειτουργικά)
- 🏠 Dashboard με XP, level, streak, coins, ημερήσια πρόκληση, weak/strong categories
- 📝 Προσομοίωση επίσημης εξέτασης (30 ερωτήσεις, 30' timer, 85% pass)
- 📖 Ελεύθερη εξάσκηση (60 ερωτήσεις — δείγμα από 400+)
- 🎯 Mistakes mode με **spaced repetition** (Leitner box, weighted resampling)
- 🗂️ Εξάσκηση κατά κατηγορία (10 κατηγορίες)
- ⭐ Bookmarks / Αγαπημένα
- 🔎 Full-text search
- 📊 Στατιστικά με Chart.js (line + bar), heatmap κατηγοριών
- 🏅 13 badges/achievements + confetti animations
- 🔥 Daily streak tracking
- 🌙 Dark mode
- 📱 Fully responsive (mobile-first)
- 💾 LocalStorage persistence (guest mode)
- 🇬🇷 ΟΛΑ στα ελληνικά

## Αρχεία
- `index.html` — Το app (single-page, vanilla JS + Tailwind CDN + Chart.js CDN)
- `questions.js` — Τράπεζα ερωτήσεων + κατηγορίες + badges
- `serve.py` — Απλός http server
- `.claude/launch.json` — Configuration για preview

## Migration σε Next.js + Supabase (production)

Το app είναι δομημένο για εύκολο port. Ακολούθησε:

### 1. Setup
```
npx create-next-app@latest drivepro --typescript --tailwind --app
cd drivepro
npm install @supabase/supabase-js @supabase/ssr framer-motion lucide-react recharts
```

### 2. Supabase schema
```sql
create table questions (id serial primary key, cat text, q text, options jsonb, correct int, explain text, tip text, image_url text);
create table user_progress (user_id uuid references auth.users, question_id int references questions, mastery_level text, streak int, next_due timestamptz, primary key (user_id, question_id));
create table user_stats (user_id uuid primary key, xp int default 0, coins int default 0, streak int default 0, longest_streak int default 0, last_active date);
create table user_badges (user_id uuid, badge_id text, earned_at timestamptz default now(), primary key (user_id, badge_id));
create table user_bookmarks (user_id uuid, question_id int, primary key (user_id, question_id));
```
Ενεργοποίησε RLS σε όλους τους πίνακες με policies `auth.uid() = user_id`.

### 3. Auth (Google + Email)
- Supabase Dashboard → Authentication → Providers → Google (client ID/secret από Google Cloud Console).
- Στα κουμπιά «Σύνδεση με Google» στο `routes.profile`: `supabase.auth.signInWithOAuth({ provider: 'google' })`
- Email: `supabase.auth.signUp({ email, password })` + email verification enabled.

### 4. State migration
Ο κώδικας χρησιμοποιεί ένα singleton `S` object. Αντικατάστησέ το με Zustand/Jotai store που συγχρονίζει με Supabase (upsert σε κάθε change).

### 5. Admin Panel (PDF Import)
- Route `/admin` προστατευμένο με RLS (role='admin' claim).
- Upload PDF → serverless function με `pdf-parse` + regex για extraction ερωτήσεων/απαντήσεων.
- Preview → manual edit → bulk insert στον `questions` πίνακα.

### 6. Deployment
- `vercel` για frontend
- Supabase managed για backend
- Cloudflare για image CDN

## Επόμενα βήματα για την τράπεζα ερωτήσεων
Οι 60 ερωτήσεις που υπάρχουν είναι πραγματικές και βασισμένες στον ΚΟΚ.
Για πλήρη κάλυψη 400+ ερωτήσεων της επίσημης εξέτασης:
1. Χρησιμοποίησε το `book_AYTOKINHTA.pdf` (Ίδρυμα Ευγενίδου) που παρέχεις
2. Το PDF χρησιμοποιεί CP1253 encoding — extract με `pdftotext` και μετά `python -c "open('out.txt','w',encoding='utf-8').write(open('in.txt','rb').read().decode('cp1253',errors='replace'))"`
3. Οι ερωτήσεις είναι κυρίως στο τελευταίο μέρος του βιβλίου (κεφάλαιο εξέτασης).

## Άδεια
Personal use. Το περιεχόμενο είναι πνευματική ιδιοκτησία του Υπουργείου Μεταφορών & Ιδρύματος Ευγενίδου.
