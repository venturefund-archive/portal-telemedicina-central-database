import rules


@rules.predicate
def does_user_has_client_assigned(user):
    if user.client:
        return True
    return False


# rules.add_rule("can_view_patient", does_user_has_client_assigned)
