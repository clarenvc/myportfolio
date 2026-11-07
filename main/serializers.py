from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Skill, Experience, Education

class SkillSerializer(serializers.ModelSerializer):
    # khusus buat star
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            "id", "tool_name", "category_title", "description",
            "tool_logo_url", "sub_skills",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_tool_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Tool cannot be a html tag")
        return value

    def validate_category_title(self, value):
        return strip_tags(value).strip()

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate_sub_skills(self, value):
        if value:
            return strip_tags(value).strip()
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = ["id", "company", "role", "description", "star_count", "is_starred"]

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.starred_by.filter(id=request.user.id).exists()
        return False

    def validate_description(self, value):
        return strip_tags(value)


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id", "school_name", "start_year", "end_year", "description",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_school_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("School name cannot be empty or only HTML tags")
        return value

    def validate_end_year(self, value):
        value = strip_tags(value).strip()
        if not (value.isdigit() or value.lower() == "present"):
            raise serializers.ValidationError('End year must be a year (e.g. "2025") or "Present"')
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())