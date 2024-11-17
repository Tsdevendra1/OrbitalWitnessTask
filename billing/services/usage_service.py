from billing.dataclasses import Credit
from billing.schemas import UsageEntry, UsageResponse
from billing.services.credit_calculation_service import CalculateCreditsService
from billing.services.messages_service import MessageService
from billing.services.reports_service import ReportService


class UsageService:
    def __init__(
        self,
        message_service: MessageService,
        report_service: ReportService,
        calculate_credits_service: CalculateCreditsService,
    ) -> None:
        self._message_service = message_service
        self._report_service = report_service
        self._calculate_credits_service = calculate_credits_service

    def get_usage(self) -> UsageResponse:
        # Assumption #1: Ordering of response not mentioned so I'm returning the usage in the order of messages fetched.
        # Assumption #2: I'm assuming API call doesn't take too long so can do this synchronously inside the request. Could
        # approach the problem differently where we pre-calculate usage (e.g. once a day) and store it to speed up this
        # request if the API call is slow.
        messages = self._message_service.fetch_messages()
        usage_data = []

        for message in messages:
            report_name = None
            if message.report_id:
                # Decision #1: If I had more time exponential back-off and retries can be added here to handle API rate limits.
                # Decision #2: If I had more time could also add parallel fetching of report data to save time using asyncio.gather, doing so outside this for loop. (NOTE: I didn't use async because of time constraints)
                # Decision #3: If I had more time could also add caching here, either using a simple dictionary or a more sophisticated cache like Redis.
                report = self._report_service.fetch_report(message.report_id)
                if report:
                    credits_used = Credit(amount=report.credit_cost)
                    report_name = report.name
                else:
                    credits_used = self._calculate_credits_service.calculate_credits(message.text)
            else:
                credits_used = self._calculate_credits_service.calculate_credits(message.text)

            usage_data.append(
                UsageEntry(
                    report_name=report_name,
                    message_id=message.id,
                    timestamp=message.timestamp,
                    credits_used=float(credits_used.amount),
                )
            )

        return UsageResponse(usage=usage_data)
