from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        
        # Delete all existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write('Creating teams...')
        
        # Create teams
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Assemble! Marvel superheroes working together for fitness excellence.'
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League members committed to peak physical performance.'
        )

        self.stdout.write('Creating users...')
        
        # Create Marvel users
        marvel_users = [
            User.objects.create(name='Iron Man', email='tony@stark.com', team_id=team_marvel.id),
            User.objects.create(name='Captain America', email='steve@rogers.com', team_id=team_marvel.id),
            User.objects.create(name='Black Widow', email='natasha@romanoff.com', team_id=team_marvel.id),
            User.objects.create(name='Thor', email='thor@asgard.com', team_id=team_marvel.id),
            User.objects.create(name='Hulk', email='bruce@banner.com', team_id=team_marvel.id),
        ]
        
        # Create DC users
        dc_users = [
            User.objects.create(name='Superman', email='clark@kent.com', team_id=team_dc.id),
            User.objects.create(name='Batman', email='bruce@wayne.com', team_id=team_dc.id),
            User.objects.create(name='Wonder Woman', email='diana@prince.com', team_id=team_dc.id),
            User.objects.create(name='Flash', email='barry@allen.com', team_id=team_dc.id),
            User.objects.create(name='Aquaman', email='arthur@curry.com', team_id=team_dc.id),
        ]

        all_users = marvel_users + dc_users

        self.stdout.write('Creating activities...')
        
        # Create activities for each user
        activity_types = ['Running', 'Swimming', 'Cycling', 'Strength Training', 'Yoga']
        
        for user in all_users:
            for i in range(10):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = random.uniform(1.0, 20.0) if activity_type in ['Running', 'Swimming', 'Cycling'] else None
                calories = duration * random.randint(5, 12)
                activity_date = date.today() - timedelta(days=random.randint(0, 30))
                
                Activity.objects.create(
                    user_id=user.id,
                    activity_type=activity_type,
                    duration=duration,
                    distance=round(distance, 2) if distance else None,
                    calories=calories,
                    date=activity_date
                )

        self.stdout.write('Creating leaderboard entries...')
        
        # Create leaderboard entries based on total calories
        for user in all_users:
            total_calories = sum(a.calories for a in Activity.objects.filter(user_id=user.id))
            Leaderboard.objects.create(
                user_id=user.id,
                points=total_calories,
                rank=0  # Will be updated after all entries are created
            )
        
        # Update ranks based on points
        leaderboard_entries = Leaderboard.objects.all().order_by('-points')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()

        self.stdout.write('Creating workouts...')
        
        # Create workout suggestions
        workouts = [
            {
                'name': 'Captain America\'s Shield Training',
                'description': 'Build strength and endurance with shield-throwing exercises',
                'difficulty': 'intermediate',
                'duration': 45,
                'category': 'Strength Training'
            },
            {
                'name': 'Flash Speed Workout',
                'description': 'High-intensity interval training to increase speed',
                'difficulty': 'advanced',
                'duration': 30,
                'category': 'Running'
            },
            {
                'name': 'Wonder Woman Warrior Training',
                'description': 'Full-body workout inspired by Amazon warriors',
                'difficulty': 'intermediate',
                'duration': 60,
                'category': 'Strength Training'
            },
            {
                'name': 'Aquaman Swimming Circuit',
                'description': 'Swimming techniques for ocean-level performance',
                'difficulty': 'advanced',
                'duration': 50,
                'category': 'Swimming'
            },
            {
                'name': 'Black Widow Agility Training',
                'description': 'Flexibility and agility exercises for spy-level fitness',
                'difficulty': 'intermediate',
                'duration': 40,
                'category': 'Yoga'
            },
            {
                'name': 'Hulk Strength Builder',
                'description': 'Maximum strength training for incredible power',
                'difficulty': 'advanced',
                'duration': 55,
                'category': 'Strength Training'
            },
            {
                'name': 'Superman Flight Training',
                'description': 'Core and cardio workout for super endurance',
                'difficulty': 'beginner',
                'duration': 35,
                'category': 'Running'
            },
            {
                'name': 'Batman Night Patrol',
                'description': 'Stealth and endurance training for crime fighters',
                'difficulty': 'intermediate',
                'duration': 45,
                'category': 'Cycling'
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with superhero test data!'))
        self.stdout.write(f'Created {User.objects.count()} users')
        self.stdout.write(f'Created {Team.objects.count()} teams')
        self.stdout.write(f'Created {Activity.objects.count()} activities')
        self.stdout.write(f'Created {Leaderboard.objects.count()} leaderboard entries')
        self.stdout.write(f'Created {Workout.objects.count()} workouts')
