# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

import pydantic


class SubjectClaimSet(pydantic.BaseModel):
    name: str | None = pydantic.Field(
        default=None,
        title="Name",
        description=(
            "End-User's full name in displayable form including all name "
            "parts, possibly including titles and suffixes, ordered "
            "according to the End-User's locale and preferences."
        )
    )

    given_name: str | None = pydantic.Field(
        default=None,
        title="Given name",
        description=(
            "Given name(s) or first name(s) of the End-User. Note that in some "
            "cultures, people can have multiple given names; all can be present, "
            "with the names being separated by space characters."
        )
    )

    family_name: str | None = pydantic.Field(
        default=None,
        title="Family name",
        description=(
            "Surname(s) or last name(s) of the End-User. Note that in some cultures, "
            "people can have multiple family names or no family name; all can be "
            "present, with the names being separated by space characters."
        )
    )

    middle_name: str | None = pydantic.Field(
        default=None,
        title="Middle name",
        description=(
            "Middle name(s) of the End-User. Note that in some cultures, people can "
            "have multiple middle names; all can be present, with the names being "
            "separated by space characters. Also note that in some cultures, middle "
            "names are not used."
        )
    )

    nickname: str | None = pydantic.Field(
        default=None,
        title="Nickname",
        description=(
            "Casual name of the End-User that may or may not be the same as "
            "the `given_name`. For instance, a `nickname` value of `Mike` "
            "might be returned alongside a `given_name` value of `Michael`."
        )
    )

    preferred_username: str | None = pydantic.Field(
        default=None,
        title="Preferred username",
        description=(
            "Shorthand name by which the End-User wishes to be referred to "
            "at the RP, such as `janedoe` or `j.doe`. This value MAY be "
            "any valid JSON string including special characters such as "
            "`@`, `/`, or whitespace. The RP MUST NOT rely upon this "
            "value being unique, as discussed in Section 5.7 of the OpenID "
            "Connect Core 1.0 specification."
        )
    )

    profile: str | None = pydantic.Field(
        default=None,
        title="Profile URL",
        description=(
            "URL of the End-User's profile page. The contents "
            "of this Web page SHOULD be about the End-User."
        )
    )

    picture: str | None = pydantic.Field(
        default=None,
        title="Picture",
        description=(
            "URL of the End-User's profile picture. This URL MUST refer "
            "to an image file (for example, a PNG, JPEG, or GIF image "
            "file), rather than to a Web page containing an image. Note "
            "that this URL SHOULD specifically reference a profile photo "
            "of the End-User suitable for displaying when describing the "
            "End-User, rather than an arbitrary photo taken by the End-User."
        )
    )

    website: str | None = pydantic.Field(
        default=None,
        title="Website",
        description=(
            "URL of the End-User's Web page or blog. This Web page SHOULD "
            "contain information published by the End-User or an organization "
            "that the End-User is affiliated with."
        )
    )

    gender: str | None = pydantic.Field(
        default=None,
        title="Gender",
        description=(
            "End-User's gender. Values defined by this specification are "
            "`female` and `male`. Other values MAY be used when neither "
            "of the defined values are applicable."
        )
    )

    birthdate: datetime.date | str | None = pydantic.Field(
        default=None,
        title="Birthdate",
        description=(
            "End-User's birthday, represented as an ISO 8601:2004 `YYYY-MM-DD` "
            "format. The year MAY be `0000`, indicating that it is omitted. "
            "To represent only the year, `YYYY` format is allowed. Note that "
            "depending on the underlying platform's date related function, "
            "providing just year can result in varying month and day, so the "
            "implementers need to take this factor into account to correctly "
            "process the dates."
        )
    )

    zoneinfo: str | None = pydantic.Field(
        default=None,
        title="Timezone",
        description=(
            "String from zoneinfo time zone database representing the "
            "End-User's time zone. For example, `Europe/Paris` or "
            "`America/Los_Angeles`."
        )
    )

    locale: str | None = pydantic.Field(
        default=None,
        title="Locale",
        description=(
            "End-User's locale, represented as a BCP47 language tag. This is "
            "typically an ISO 639-1 Alpha-2 language code in lowercase and "
            "an ISO 3166-1 Alpha-2 country code in uppercase, separated by "
            "a dash. For example, `en-US` or `fr-CA`. As a compatibility "
            "note, some implementations have used an underscore as the "
            "separator rather than a dash, for example, `en_US`; "
            "Relying Parties MAY choose to accept this locale syntax as well."
        )
    )