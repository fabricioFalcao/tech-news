import pytest
from unittest.mock import patch, MagicMock
from tech_news.analyzer.reading_plan import ReadingPlanService

# Test case data
news_data = [
    {"title": "News 1", "reading_time": 5},
    {"title": "News 2", "reading_time": 10},
    {"title": "News 3", "reading_time": 15},
    {"title": "News 4", "reading_time": 20},
]


def test_reading_plan_group_news():
    # Test that an exception is raised for invalid available_time
    with pytest.raises(
        ValueError, match="Valor 'available_time' deve ser maior que zero"
    ):
        ReadingPlanService.group_news_for_available_time(0)
    with pytest.raises(
        ValueError, match="Valor 'available_time' deve ser maior que zero"
    ):
        ReadingPlanService.group_news_for_available_time(-1)

    # Mocking the _db_news_proxy method
    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy"
    ) as mock_db_news_proxy:
        # Test case with specific news items
        mock_db_news_proxy.return_value = news_data.copy()

        # Test case where all news items are readable
        result = ReadingPlanService.group_news_for_available_time(30)
        assert len(result["readable"]) == 3
        assert len(result["unreadable"]) == 0

        # Test case where all news items are unreadable
        result = ReadingPlanService.group_news_for_available_time(1)
        assert len(result["readable"]) == 0
        assert len(result["unreadable"]) == 4

        # Test case where some news items are readable and some are unreadable
        result = ReadingPlanService.group_news_for_available_time(10)
        assert len(result["readable"]) == 2
        assert len(result["unreadable"]) == 2

        # Validate the 'unfilled_time' in 'readable'
        assert result["readable"][0]["unfilled_time"] == 5  # 10 - 5
        assert result["readable"][1]["unfilled_time"] == 0  # 10 - 10

        # Validate the 'chosen_news' in 'readable'
        assert result["readable"][0]["chosen_news"] == [("News 1", 5)]
        assert result["readable"][1]["chosen_news"] == [("News 2", 10)]

        # Validate the 'unreadable' list
        assert result["unreadable"] == [("News 3", 15), ("News 4", 20)]

        # Test case with no news items
        mock_db_news_proxy.return_value = []
        result = ReadingPlanService.group_news_for_available_time(10)
        assert result == {"readable": [], "unreadable": []}

        # Test case with news items exactly fitting into available time
        mock_db_news_proxy.return_value = news_data.copy()
        result = ReadingPlanService.group_news_for_available_time(50)
        assert len(result["readable"]) == 2
        assert len(result["unreadable"]) == 0

        # Test case with news items exceeding available time
        result = ReadingPlanService.group_news_for_available_time(10)
        assert len(result["readable"]) == 2
        assert len(result["unreadable"]) == 2


# Run the tests
if __name__ == "__main__":
    pytest.main()
