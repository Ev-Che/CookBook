def user_register(user_form):
    # Create a new user object but avoid saving it yet
    new_user = user_form.save(commit=False)
    # Set a chosen password. set_password added encryption.
    new_user.set_password(
        user_form.cleaned_data['password'])
    # Save the User object
    new_user.save()
    return new_user
