def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_dictionary(client):
    # Arrange

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"

    verify_response = client.get("/activities")
    assert email in verify_response.json()[activity_name]["participants"]


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_removes_student(client):
    # Arrange
    activity_name = "Gym Class"
    email = "olivia@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participant", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Removed {email} from {activity_name}"

    verify_response = client.get("/activities")
    assert email not in verify_response.json()[activity_name]["participants"]


def test_remove_missing_participant_returns_400(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "unknown@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participant", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
