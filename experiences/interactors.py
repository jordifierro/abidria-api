from experiences.entities import Experience


class GetAllExperiencesInteractor(object):

    def __init__(self, experience_repo, permissions_validator):
        self.experience_repo = experience_repo
        self.permissions_validator = permissions_validator

    def set_params(self, logged_person_id):
        self.logged_person_id = logged_person_id
        return self

    def execute(self):
        self.permissions_validator.validate_permissions(logged_person_id=self.logged_person_id)

        return self.experience_repo.get_all_experiences()


class CreateNewExperienceInteractor(object):

    def __init__(self, experience_repo, experience_validator, permissions_validator):
        self.experience_repo = experience_repo
        self.experience_validator = experience_validator
        self.permissions_validator = permissions_validator

    def set_params(self, title, description, logged_person_id):
        self.title = title
        self.description = description
        self.logged_person_id = logged_person_id
        return self

    def execute(self):
        self.permissions_validator.validate_permissions(logged_person_id=self.logged_person_id,
                                                        wants_to_create_content=True)
        experience = Experience(title=self.title, description=self.description, author_id=self.logged_person_id)
        self.experience_validator.validate_experience(experience)
        return self.experience_repo.create_experience(experience)


class ModifyExperienceInteractor(object):

    def __init__(self, experience_repo, experience_validator, permissions_validator):
        self.experience_repo = experience_repo
        self.experience_validator = experience_validator
        self.permissions_validator = permissions_validator

    def set_params(self, id, title, description, logged_person_id):
        self.id = id
        self.title = title
        self.description = description
        self.logged_person_id = logged_person_id
        return self

    def execute(self):
        self.permissions_validator.validate_permissions(logged_person_id=self.logged_person_id,
                                                        has_permissions_to_modify_experience=self.id)
        experience = self.experience_repo.get_experience(id=self.id)

        new_title = self.title if self.title is not None else experience.title
        new_description = self.description if self.description is not None else experience.description
        updated_experience = Experience(id=experience.id, title=new_title,
                                        description=new_description, author_id=experience.author_id)

        self.experience_validator.validate_experience(updated_experience)

        return self.experience_repo.update_experience(updated_experience)
