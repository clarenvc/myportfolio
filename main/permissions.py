from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    message = "Only the portfolio owner or an editor can change this data."

    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if request.method in ("PUT", "PATCH"):
            return bool(request.user and 
                request.user.is_authenticated and 
                request.user.groups.filter(name="Editor").exists()
            )
        
        return False