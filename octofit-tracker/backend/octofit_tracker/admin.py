from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'team_id', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'activity_type', 'duration', 'distance', 'calories', 'date', 'created_at']
    search_fields = ['activity_type']
    list_filter = ['activity_type', 'date', 'created_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'points', 'rank', 'updated_at']
    list_filter = ['updated_at']
    ordering = ['rank']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'difficulty', 'duration', 'category', 'created_at']
    search_fields = ['name', 'category']
    list_filter = ['difficulty', 'category', 'created_at']
