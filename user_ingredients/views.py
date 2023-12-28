from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ingredients.forms import IngredientsForm
from ingredients.models import Ingredient
from products.models import Product

from .models import UserIngredient


def find_ingredient(form: dict) -> [Ingredient, bool]:
    ingredient, created = Ingredient.objects.get_or_create(
        product=form.get("product_name"),
        quantity_type=form.get("quantity_type"),
    )
    return ingredient, created


class UserIngredientsHomePageView(LoginRequiredMixin, ListView):
    model = UserIngredient
    template_name = "useringredients/home.html"
    extra_context = {"title": "My Ingredients"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        context["useringredients"] = self.model.objects.filter(
            user=request.user.profile.id
        )
        return render(request, self.template_name, context)


class UserIngredientsAddPageView(LoginRequiredMixin, CreateView):
    model = UserIngredient
    form_class = IngredientsForm
    template_name = "useringredients/ingredient_form.html"
    extra_context = {"title": "Add My Ingredient"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        if kwargs.get("product_id"):
            product_id = kwargs.get("product_id")
            context["form"] = self.form_class(initial={"product_name": product_id})
        else:
            context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if "add_product" in request.POST:
            return redirect("products:product-add", "new")
        if form.is_valid():
            ingredient, created = find_ingredient(form.cleaned_data)
            did_user_have_ingredient = UserIngredient.objects.get(
                ingredients=ingredient
            )
            if did_user_have_ingredient:
                did_user_have_ingredient.amount += form.cleaned_data.get("amount")
                did_user_have_ingredient.save()
                messages.success(
                    request,
                    f"{did_user_have_ingredient.ingredients.product.name} has been added previously. Amount was updated",
                )
            else:
                self.model.objects.get_or_create(
                    user=request.user.profile,
                    ingredients=ingredient,
                    amount=form.cleaned_data.get("amount"),
                )
                messages.success(request, "My Ingredient has been successfully added")
            return redirect("my_ingredients:useringredients-home-page")
        else:
            messages.warning(request, "Invalid data in my ingredients")
            return redirect("my_ingredients:useringredient-add")


class UserIngredientsEditPageView(LoginRequiredMixin, UpdateView):
    model = UserIngredient
    form_class = IngredientsForm
    template_name = "useringredients/ingredient_form.html"
    extra_context = {"title": "Edit My Ingredient"}

    def get(self, request, *args, **kwargs):
        my_ingredient_id = kwargs.get("my_ingredient_id")
        my_ingredient = get_object_or_404(self.model, pk=my_ingredient_id)
        context = self.extra_context
        if kwargs.get("product_id"):
            product_id = kwargs.get("product_id")
            my_ingredient.ingredients.product = Product.objects.get(id=product_id)
        context["form"] = self.form_class(
            initial={
                "product_name": my_ingredient.ingredients.product,
                "quantity_type": my_ingredient.ingredients.quantity_type,
                "amount": my_ingredient.amount,
            }
        )
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        my_ingredient_id = kwargs.get("my_ingredient_id")
        form = self.form_class(request.POST)
        if "add_product" in request.POST:
            return redirect("products:product-add", my_ingredient_id)
        if form.is_valid():
            ingredient, created = find_ingredient(form.cleaned_data)
            self.model.objects.filter(id=my_ingredient_id).update(
                ingredients=ingredient, amount=form.cleaned_data.get("amount")
            )
            messages.success(request, "Successfully edited my ingredient")
            return redirect("my_ingredients:useringredients-home-page")
        else:
            messages.warning(request, "Invalid data in editing my ingredient")
            return redirect("my_ingredients:useringredient-edit", my_ingredient_id)


class UserIngredientsDeletePageView(LoginRequiredMixin, DeleteView):
    model = UserIngredient

    def get_success_url(self):
        success_url = reverse("my_ingredients:useringredients-home-page")
        return success_url

    def form_valid(self, form):
        messages.success(self.request, "Successfully removed my ingredient")
        return super().form_valid(form)
