"""Seed the database with fictional demo content for client demos.

Everything generated here (usernames, article text, comments) is invented
for demonstration purposes only and is not based on any real person, place,
or event. Safe to run repeatedly - existing demo records are reused rather
than duplicated.
"""

import random
from datetime import date

from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import Article, Category, Comment, Reply, UserFavoriteCategory
from users.models import User

DEMO_PASSWORD = "HorizonDemo2026!"

CATEGORIES = ["World", "Business", "Technology", "Sports", "Entertainment", "Health", "Science"]

# Fictional newsroom staff (bylines). None of these correspond to real people.
AUTHORS = [
    ("a.rowntree", "Asha", "Rowntree", "a.rowntree@horizonnews.example"),
    ("m.solberg", "Mateo", "Solberg", "m.solberg@horizonnews.example"),
    ("l.nakamura", "Lena", "Nakamura", "l.nakamura@horizonnews.example"),
    ("d.okafor", "Dara", "Okafor", "d.okafor@horizonnews.example"),
    ("t.vance", "Theo", "Vance", "t.vance@horizonnews.example"),
    ("s.kowalski", "Sanne", "Kowalski", "s.kowalski@horizonnews.example"),
]

# Fictional reader accounts used to demo login, favorites, comments and replies.
READERS = [
    ("demo_reader1", "Priya", "Chen", "priya.demo@horizonnews.example"),
    ("demo_reader2", "Marcus", "Webb", "marcus.demo@horizonnews.example"),
    ("demo_reader3", "Isla", "Fontaine", "isla.demo@horizonnews.example"),
]

ADMIN_USERNAME = "demo_admin"
ADMIN_EMAIL = "admin@horizonnews.example"

# Fictional places/organisations used across articles so nothing resembles
# a real-world entity.
PLACES = ["Caldera Bay", "Meridian Coast", "Northgate", "Silversea", "Amberfield", "Rosthwaite"]
ORGS = ["the Caldera Trade Council", "Northgate Analytics", "the Meridian Institute", "Amberfield Labs", "the Rosthwaite Federation"]

ARTICLES = {
    "World": [
        ("Caldera Bay Reaches New Trade Agreement With Neighboring Region",
         "Officials in {place} signed a wide-ranging trade agreement this week aimed at reducing tariffs on agricultural goods. "
         "Representatives from {org} said the deal, years in the making, should lower food prices for residents within the next fiscal year.\n\n"
         "Critics have raised concerns about the pace of implementation, while supporters argue the agreement will strengthen regional supply chains "
         "that were disrupted in recent seasons."),
        ("Flooding Prompts Evacuations Along the {place} River Basin",
         "Heavy rainfall over the past week has forced hundreds of families to evacuate low-lying neighborhoods near {place}. "
         "Emergency services report no major injuries so far, though several roads remain impassable.\n\n"
         "Local authorities have opened three temporary shelters and are coordinating with {org} to assess long-term flood defenses."),
        ("Diplomatic Talks Resume Between Regional Councils",
         "After a six-month pause, delegates from {place} and neighboring territories have resumed talks intended to resolve a long-standing border dispute.\n\n"
         "Analysts at {org} describe the renewed dialogue as a cautiously positive sign, though they caution that previous rounds of talks have stalled over similar issues."),
        ("Population Growth Slows Across Coastal Cities",
         "New census figures show population growth in {place} has slowed for the third consecutive year, a trend demographers attribute to rising housing costs.\n\n"
         "{org} released a report suggesting the shift could ease pressure on public transit but may strain the local labor market in coming years."),
    ],
    "Business": [
        ("Regional Retailers Report Strongest Quarter in Five Years",
         "Retail chains headquartered in {place} posted their strongest quarterly earnings since records began tracking the sector, according to a filing reviewed by our newsroom.\n\n"
         "Executives credited improved logistics and a rebound in consumer spending, while analysts at {org} noted that rising wages may squeeze margins later this year."),
        ("Startup Funding in the Region Rebounds After Two-Year Slump",
         "Venture investment in {place}-based startups climbed sharply last quarter, reversing a two-year downward trend.\n\n"
         "{org} attributes the rebound to renewed investor confidence in logistics and clean-energy startups, sectors that had struggled to raise capital in prior years."),
        ("Manufacturers Warn of Continued Supply Chain Pressures",
         "Several manufacturers based near {place} say they continue to face delays sourcing key components, despite broader improvements across the industry.\n\n"
         "A spokesperson for {org} said the bottlenecks are concentrated in specialized electronics, with lead times still double pre-disruption levels."),
        ("Local Currency Strengthens Against Regional Peers",
         "The currency used across {place} strengthened for a fourth straight week, a move economists link to higher-than-expected export figures.\n\n"
         "Officials at {org} say the trend could make imports cheaper for consumers but may weigh on export-driven manufacturers."),
    ],
    "Technology": [
        ("Local Startup Unveils Battery With Faster Charging Cycle",
         "A small engineering team based in {place} has unveiled a prototype battery cell that it claims charges to 80 percent capacity in under ten minutes.\n\n"
         "Independent reviewers have not yet verified the claims, but {org} says early lab tests show promising results for use in public transit fleets."),
        ("Regional Broadband Rollout Reaches Rural Communities",
         "A multi-year effort to extend high-speed broadband into rural areas surrounding {place} has reached its halfway milestone, project leaders announced Tuesday.\n\n"
         "{org} estimates the remaining phases will connect an additional forty thousand households within two years."),
        ("New Data Privacy Rules Take Effect for Regional Apps",
         "Developers operating in {place} must now comply with updated data-handling rules requiring clearer consent screens and shorter retention periods.\n\n"
         "{org} says the rules were designed after consultation with local developers, though some smaller studios have asked for a longer transition window."),
        ("Robotics Lab Opens Public Demonstration Facility",
         "A robotics research lab in {place} has opened a public demonstration space where visitors can watch prototype delivery robots navigate mock city streets.\n\n"
         "Researchers with {org} hope the exhibit will demystify automation technology ahead of a planned pilot program next year."),
    ],
    "Sports": [
        ("Coastal Rowing Club Wins Regional Championship",
         "The Caldera Bay rowing club claimed its first regional championship in over a decade, edging out a strong field in near-perfect conditions.\n\n"
         "Coaches credited a rebuilt training program and a younger roster for the turnaround after several difficult seasons."),
        ("Local League Introduces Expanded Playoff Format",
         "Organizers of the {place} amateur league announced an expanded playoff format for the upcoming season, adding two wildcard slots.\n\n"
         "The change follows feedback from clubs who argued the previous format eliminated too many competitive teams too early."),
        ("Youth Academy Graduates First Professional Player",
         "A youth football academy based near {place} celebrated its first graduate to sign a professional contract, a milestone the academy's founders called validation of their grassroots approach.\n\n"
         "The academy, supported in part by {org}, plans to expand its coaching staff next season."),
        ("Marathon Route Changed After Community Feedback",
         "Organizers of the annual {place} marathon confirmed a revised route for this year's race after residents raised concerns about road closures near the harbor.\n\n"
         "The new course adds a scenic stretch along the waterfront while reducing disruption to weekday traffic."),
    ],
    "Entertainment": [
        ("Independent Film Festival Announces Record Submissions",
         "The annual independent film festival held in {place} received a record number of submissions this year, organizers announced, with entries from first-time directors up sharply.\n\n"
         "Festival programmers say the growth reflects wider access to affordable filmmaking equipment and editing software."),
        ("Local Theater Revives Classic Production for Anniversary Season",
         "A theater company in {place} will revive a beloved production as part of its anniversary season, featuring a mostly new cast alongside a handful of returning performers.\n\n"
         "Tickets for the opening weekend sold out within hours of going on sale."),
        ("Streaming Series Filmed in Region Draws International Attention",
         "A drama series filmed largely on location near {place} has drawn unexpected international attention after clips circulated widely online.\n\n"
         "Local tourism officials say they have already seen a small uptick in inquiries from visitors hoping to see filming locations."),
        ("Music Venue Reopens After Renovation",
         "A long-running music venue in {place} reopened its doors this week following an extensive renovation funded partly by community donations.\n\n"
         "Organizers say the upgraded space will allow for larger touring acts while preserving the venue's original character."),
    ],
    "Health": [
        ("Regional Clinics Expand Access to Telehealth Appointments",
         "A network of community clinics serving {place} has expanded telehealth availability, aiming to reduce wait times for routine consultations.\n\n"
         "{org} reports early data showing shorter average wait times, though officials caution it is too early to draw firm conclusions."),
        ("Study Links Commute Times to Reported Sleep Quality",
         "A study conducted among residents of {place} found a correlation between longer commute times and self-reported sleep quality, though researchers stopped short of claiming causation.\n\n"
         "The authors, affiliated with {org}, say further research is needed before any policy recommendations can be made."),
        ("Community Health Fair Draws Record Attendance",
         "An annual health fair in {place} drew record attendance this year, with organizers offering free screenings and vaccination clinics.\n\n"
         "Volunteers said demand for blood pressure and vision screenings was especially high among older attendees."),
        ("New Guidelines Issued for Seasonal Allergy Management",
         "Health officials serving {place} issued updated guidance for managing seasonal allergies, citing a longer pollen season observed in recent years.\n\n"
         "{org} recommends residents with chronic symptoms consult a clinician before the season peaks."),
    ],
    "Science": [
        ("Marine Researchers Document Coral Recovery Near {place}",
         "A team of marine biologists monitoring reefs near {place} reported early signs of coral recovery following a multi-year restoration project.\n\n"
         "Researchers with {org} caution that recovery remains fragile and highly dependent on water temperatures over the next several summers."),
        ("Local Observatory Captures Rare Meteor Shower Footage",
         "An observatory near {place} captured detailed footage of a meteor shower visible across the region last weekend, drawing interest from amateur astronomers.\n\n"
         "Staff say the footage will be used in an upcoming public exhibit on seasonal night-sky events."),
        ("Soil Study Suggests New Approach to Regional Farming",
         "A multi-year soil study conducted near {place} suggests that rotating cover crops could improve yields without increasing water usage.\n\n"
         "{org} plans to share the findings with regional farming cooperatives ahead of the next planting season."),
        ("Researchers Track Migratory Bird Patterns Using New Sensors",
         "Scientists monitoring migratory birds near {place} have deployed lightweight tracking sensors that provide more precise data on flight paths than previous methods.\n\n"
         "Early results from {org} suggest some species are shifting their routes earlier in the season than historical averages predicted."),
    ],
}

READER_COMMENTS = [
    "Really informative piece, thanks for covering this.",
    "I hadn't seen this reported anywhere else - appreciate the detail.",
    "Curious to see how this develops over the next few months.",
    "This matches what I've been noticing locally too.",
    "Would love a follow-up article once there's more data.",
    "Balanced reporting, thanks for including both perspectives.",
]

READER_REPLIES = [
    "Agreed, this is worth keeping an eye on.",
    "Good point - hadn't thought of it that way.",
    "Same here, following this closely.",
    "Thanks for the reply, that clarifies it.",
]


class Command(BaseCommand):
    help = "Populate the database with fictional demo data (categories, articles, users, comments)."

    def handle(self, *args, **options):
        random.seed(42)

        categories = self._seed_categories()
        authors = self._seed_authors()
        readers = self._seed_readers()
        self._seed_admin()
        articles = self._seed_articles(categories, authors)
        self._seed_favorites(readers, categories)
        self._seed_comments(articles, readers)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(categories)} categories, {Article.objects.count()} articles, "
            f"{len(authors)} author accounts and {len(readers)} reader accounts."
        ))

    def _seed_categories(self):
        categories = {}
        for name in CATEGORIES:
            category, _ = Category.objects.get_or_create(name=name)
            categories[name] = category
        return categories

    def _seed_authors(self):
        authors = []
        for username, first, last, email in AUTHORS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"first_name": first, "last_name": last, "email": email},
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save()
            authors.append(user)
        return authors

    def _seed_readers(self):
        readers = []
        for username, first, last, email in READERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "email": email,
                    "date_of_birth": date(1996, 4, 12),
                },
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save()
            readers.append(user)
        return readers

    def _seed_admin(self):
        if not User.objects.filter(username=ADMIN_USERNAME).exists():
            User.objects.create_superuser(ADMIN_USERNAME, ADMIN_EMAIL, DEMO_PASSWORD)

    def _seed_articles(self, categories, authors):
        created_articles = []
        for category_name, entries in ARTICLES.items():
            category = categories[category_name]
            for title_template, body_template in entries:
                place = random.choice(PLACES)
                org = random.choice(ORGS)
                title = title_template.format(place=place)
                body = body_template.format(place=place, org=org)
                article, created = Article.objects.get_or_create(
                    title=title,
                    category=category,
                    defaults={"content": body, "author": random.choice(authors)},
                )
                created_articles.append(article)
        return created_articles

    def _seed_favorites(self, readers, categories):
        category_list = list(categories.values())
        for reader in readers:
            for category in random.sample(category_list, k=3):
                UserFavoriteCategory.objects.get_or_create(user=reader, category=category)

    def _seed_comments(self, articles, readers):
        sample_articles = random.sample(articles, k=min(12, len(articles)))
        for article in sample_articles:
            commenter = random.choice(readers)
            comment, created = Comment.objects.get_or_create(
                article=article,
                user=commenter,
                text=random.choice(READER_COMMENTS),
            )
            if created and random.random() < 0.5:
                replier = random.choice([r for r in readers if r != commenter] or readers)
                Reply.objects.get_or_create(
                    comment=comment,
                    user=replier,
                    text=random.choice(READER_REPLIES),
                )
