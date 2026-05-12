import hashlib
import html
import random
import re
import textwrap
from datetime import datetime

import streamlit as st


st.set_page_config(
    page_title="Bathhouse Employment Contract",
    page_icon="♨",
    layout="wide",
    initial_sidebar_state="expanded",
)


BATHHOUSE_ROLES = [
    {
        "title": "Boiler Room Coal Runner",
        "description": "Carry enchanted coal chips to the boiler room and keep the pipes awake through the steam-heavy night.",
    },
    {
        "title": "Herbal Soak Apprentice",
        "description": "Sort fragrant bath tokens and prepare restorative blends for guests with unusual aches and older-than-usual bones.",
    },
    {
        "title": "River Guest Attendant",
        "description": "Guide muddy river visitors to the deep-cleaning baths and record all recovered objects in the ledger.",
    },
    {
        "title": "Spirit Towel Steward",
        "description": "Fold warm towels, replace vanishing linens, and pretend not to notice when the stacks rearrange themselves.",
    },
    {
        "title": "Night Shift Lamp Lighter",
        "description": "Light the corridor lanterns at dusk and whisper the closing inventory to each flame before dawn.",
    },
    {
        "title": "Soot Sprite Snack Clerk",
        "description": "Distribute star-shaped sugar rations and keep the soot workers from unionizing during peak hours.",
    },
    {
        "title": "Elevator Etiquette Monitor",
        "description": "Escort guests between floors while maintaining silence, posture, and plausible deniability.",
    },
    {
        "title": "Steam Vent Cartographer",
        "description": "Map shifting pipes, label dangerous valves, and update the bathhouse floor plan when the walls disagree.",
    },
    {
        "title": "Guest Ledger Copyist",
        "description": "Transcribe arrivals, debts, favors, and missing names in red ink that dries only after sunset.",
    },
    {
        "title": "Kitchen Dumpling Runner",
        "description": "Rush midnight orders across the bridge and never ask why some plates return cleaner than porcelain should be.",
    },
    {
        "title": "Bath Token Auditor",
        "description": "Count, sort, and authenticate bath tokens according to a policy manual no employee has finished reading.",
    },
    {
        "title": "Bridge Crossing Usher",
        "description": "Manage arrivals on the bridge, remind workers not to breathe at the wrong moment, and keep the line moving.",
    },
    {
        "title": "Rain Bucket Dispatcher",
        "description": "Place buckets beneath mysterious leaks and file weather reports for rooms that are technically indoors.",
    },
    {
        "title": "Aromatic Salt Archivist",
        "description": "Catalog rare bath salts by scent, moon phase, and the dreams they cause in exhausted attendants.",
    },
    {
        "title": "Customer Complaint Medium",
        "description": "Receive grievances from visible and invisible guests, then translate them into actionable bathhouse paperwork.",
    },
    {
        "title": "Porcelain Tub Polisher",
        "description": "Scrub ceremonial tubs until they reflect not your face, but your most recent unpaid obligation.",
    },
    {
        "title": "Furnace Bell Scheduler",
        "description": "Ring the furnace bells on the quarter hour, except when the quarter hour rings first.",
    },
    {
        "title": "Moonlit Inventory Clerk",
        "description": "Count supplies that appear only after midnight and submit totals before they become imaginary again.",
    },
]


NAME_SYLLABLES = [
    "A",
    "Chi",
    "E",
    "Ha",
    "Ka",
    "Ko",
    "Ma",
    "Mi",
    "Na",
    "No",
    "Ra",
    "Ren",
    "Sa",
    "Sen",
    "Shi",
    "So",
    "Ta",
    "Tsu",
    "Yu",
    "Zu",
]


def inject_css() -> None:
    """Add a visual layer that evokes parchment, red seals, and signing software."""
    render_html(
        """
        <style>
            :root {
                --ink: #241915;
                --muted: #6f6259;
                --paper: #fff5dd;
                --paper-deep: #ead4a8;
                --seal: #a32020;
                --gold: #b8892f;
                --line: rgba(72, 45, 28, 0.22);
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(184, 137, 47, 0.13), transparent 34rem),
                    linear-gradient(180deg, #f4f0e8 0%, #ded5c6 100%);
                color: var(--ink);
            }

            [data-testid="stSidebar"] {
                background: #27211d;
                color: #f8efd8;
            }

            [data-testid="stSidebar"] * {
                color: #f8efd8;
            }

            .main .block-container {
                max-width: 1120px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .topbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                padding: 0.85rem 1rem;
                margin-bottom: 1.25rem;
                border: 1px solid rgba(36, 25, 21, 0.12);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.72);
                box-shadow: 0 8px 24px rgba(36, 25, 21, 0.08);
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 0.7rem;
                font-weight: 700;
                letter-spacing: 0;
            }

            .brand-mark {
                display: inline-grid;
                place-items: center;
                width: 2rem;
                height: 2rem;
                border-radius: 4px;
                background: var(--seal);
                color: #fff5dd;
                font-weight: 900;
            }

            .status-pill {
                border: 1px solid rgba(35, 104, 68, 0.34);
                background: rgba(35, 104, 68, 0.09);
                color: #245d3e;
                border-radius: 999px;
                padding: 0.28rem 0.7rem;
                font-size: 0.86rem;
                font-weight: 700;
                white-space: nowrap;
            }

            .hero {
                margin: 0.4rem 0 1.3rem;
            }

            .hero h1 {
                font-size: clamp(1.8rem, 6vw, 4.3rem);
                line-height: 0.95;
                color: #211510;
                letter-spacing: 0;
            }

            .hero p {
                margin: 0;
                color: #5e5047;
                font-size: 1.12rem;
            }

            .document-shell {
                position: relative;
                padding: clamp(1.15rem, 3vw, 2.1rem);
                border: 1px solid rgba(36, 25, 21, 0.16);
                border-radius: 8px;
                background:
                    linear-gradient(90deg, rgba(163, 32, 32, 0.08) 0 0.6rem, transparent 0.6rem),
                    linear-gradient(180deg, var(--paper) 0%, #f9e7bf 100%);
                box-shadow: 0 24px 55px rgba(36, 25, 21, 0.18);
                overflow: hidden;
            }

            .confirmation-shell {
                min-height: 34rem;
                animation: document-arrival 520ms cubic-bezier(0.18, 0.82, 0.26, 1) both;
            }

            .confirmation-shell::after {
                content: "";
                position: absolute;
                inset: 0;
                background:
                    radial-gradient(circle at 50% 8.5rem, rgba(163, 32, 32, 0.26), transparent 13rem),
                    linear-gradient(180deg, rgba(255, 245, 221, 0), rgba(255, 245, 221, 0.34));
                opacity: 0;
                pointer-events: none;
                animation: impact-flash 760ms 900ms ease-out both;
                z-index: 2;
            }

            .document-shell::before {
                content: "";
                position: absolute;
                inset: 0;
                background-image:
                    linear-gradient(var(--line) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(184, 137, 47, 0.12) 1px, transparent 1px);
                background-size: 100% 3.6rem, 3.6rem 100%;
                opacity: 0.26;
                pointer-events: none;
            }

            .document-inner {
                position: relative;
                z-index: 1;
            }

            .contract-meta {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem;
                margin-bottom: 1.35rem;
                color: var(--muted);
                font-size: 0.9rem;
            }

            .meta-box {
                border: 1px solid rgba(36, 25, 21, 0.16);
                border-radius: 6px;
                padding: 0.65rem 0.75rem;
                background: rgba(255, 251, 239, 0.68);
            }

            .meta-box strong {
                display: block;
                color: var(--ink);
                font-size: 0.96rem;
            }

            .contract-title {
                border-top: 2px solid rgba(36, 25, 21, 0.55);
                padding: 0.85rem 0;
                text-align: center;
                position: relative;
            }

            .contract-title::after {
                content: "";
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 575px; /* This is your "border length" */
                border-bottom: 2px solid black;
                }

            .contract-name {
                border-bottom: 2px solid rgba(36, 25, 21, 0.55);
                padding: 0.85rem 0;
                margin-bottom: 1.00rem;
                text-align: center;
            }

            .contract-name h2 {
                margin: 0;
                font-size: clamp(1.45rem, 4vw, 2.25rem);
                letter-spacing: 0.03em;
            }

            .contract-title h2 {
                margin: 0;
                font-size: clamp(1.45rem, 4vw, 2.25rem);
                letter-spacing: 0.03em;
            }
            .contract-title h3 {
                margin: 0;
                font-size: clamp(1.20rem, 4vw, 2.0rem);
                letter-spacing: 0.03em;
            }

            .clauses {
                counter-reset: clause;
                display: grid;
                gap: 0.85rem;
                margin: 1rem 0 1.4rem;
            }

            .clause {
                display: grid;
                grid-template-columns: 2.1rem 1fr;
                gap: 0.75rem;
                align-items: start;
                color: #3b2a21;
            }

            .clause::before {
                counter-increment: clause;
                content: counter(clause, decimal-leading-zero);
                color: var(--seal);
                font-weight: 800;
                font-size: 0.85rem;
                padding-top: 0.12rem;
            }

            .signature-line {
                margin-top: 1rem;
                border-top: 1px solid rgba(36, 25, 21, 0.42);
                padding-top: 0.5rem;
                color: var(--muted);
                font-size: 0.9rem;
            }

            .stamp-zone {
                position: relative;
                height: clamp(7rem, 18vw, 11rem);
                display: grid;
                place-items: center;
                margin: -0.2rem 0 0.4rem;
                isolation: isolate;
            }

            .stamp-zone::before,
            .stamp-zone::after {
                content: "";
                position: absolute;
                top: 50%;
                width: min(24vw, 10rem);
                border-top: 2px solid rgba(163, 32, 32, 0.44);
                opacity: 0;
                transform: scaleX(0);
                animation: impact-lines 680ms 940ms ease-out both;
            }

            .stamp-zone::before {
                right: calc(50% + 7rem);
                transform-origin: right center;
            }

            .stamp-zone::after {
                left: calc(50% + 7rem);
                transform-origin: left center;
            }

            .accepted-stamp {
                display: inline-block;
                border: 0.24rem solid var(--seal);
                color: var(--seal);
                padding: 0.38rem 0.95rem;
                font-size: clamp(2rem, 6vw, 4rem);
                font-weight: 900;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                opacity: 0;
                mix-blend-mode: multiply;
                filter: drop-shadow(0 1.25rem 0 rgba(98, 23, 18, 0.08));
                transform-origin: 50% 50%;
                animation: stamp-slam 1180ms 540ms cubic-bezier(0.08, 0.9, 0.12, 1) both;
                z-index: 3;
            }

            .confirmation-shell .contract-meta,
            .confirmation-shell .contract-title,
            .confirmation-shell .contract-name,
            .confirmation-shell .assignment-grid,
            .confirmation-shell .clauses,
            .confirmation-shell .signature-line {
                animation: details-settle 520ms 180ms ease-out both;
            }

            .assignment-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.85rem;
                margin: 1rem 0;
            }

            .assignment-box {
                border: 1px solid rgba(36, 25, 21, 0.18);
                border-radius: 6px;
                background: rgba(255, 251, 239, 0.68);
                padding: 1rem;
            }

            .assignment-box span {
                display: block;
                color: var(--muted);
                font-size: 0.88rem;
                margin-bottom: 0.2rem;
            }

            .assignment-box strong {
                font-size: 1.45rem;
            }

            .footer-note {
                margin-top: 1.5rem;
                color: #5d4d42;
                font-size: 0.92rem;
                text-align: center;
            }

            .stButton > button {
                width: 100%;
                border-radius: 6px;
                border: 1px solid #711c1c;
                background: #9f2424;
                color: white;
                font-weight: 800;
                min-height: 3rem;
            }

            .stButton > button:hover {
                border-color: #4e1111;
                background: #811c1c;
                color: white;
            }

            @keyframes document-arrival {
                0% {
                    opacity: 0;
                    transform: translateY(1.2rem) scale(0.985);
                    filter: blur(2px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                    filter: blur(0);
                }
            }

            @keyframes details-settle {
                0% {
                    opacity: 0;
                    transform: translateY(0.5rem);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes stamp-slam {
                0% {
                    opacity: 0;
                    transform: translateY(-18rem) scale(1.45) rotate(-18deg);
                    filter: blur(3px) drop-shadow(0 2.5rem 1rem rgba(98, 23, 18, 0.14));
                }
                54% {
                    opacity: 1;
                    transform: translateY(0.65rem) scale(0.86) rotate(-7deg);
                    filter: blur(0) drop-shadow(0 0.35rem 0 rgba(98, 23, 18, 0.18));
                }
                62% {
                    transform: translateY(-0.28rem) scale(1.06) rotate(-7deg);
                }
                70% {
                    transform: translateY(0.16rem) scale(0.98) rotate(-7deg);
                }
                78% {
                    transform: translateY(0) scale(1.01) rotate(-7deg);
                }
                86% {
                    transform: translateX(-0.08rem) rotate(-7.8deg);
                }
                92% {
                    transform: translateX(0.08rem) rotate(-6.4deg);
                }
                100% {
                    opacity: 0.94;
                    transform: translateX(0) translateY(0) scale(1) rotate(-7deg);
                    filter: blur(0) drop-shadow(0 0.15rem 0 rgba(98, 23, 18, 0.16));
                }
            }

            @keyframes impact-flash {
                0%,
                48% {
                    opacity: 0;
                }
                52% {
                    opacity: 1;
                }
                100% {
                    opacity: 0;
                }
            }

            @keyframes impact-lines {
                0%,
                45% {
                    opacity: 0;
                    transform: scaleX(0);
                }
                52% {
                    opacity: 0.75;
                    transform: scaleX(1);
                }
                100% {
                    opacity: 0;
                    transform: scaleX(1.2);
                }
            }

            @media (prefers-reduced-motion: reduce) {
                .confirmation-shell,
                .confirmation-shell::after,
                .confirmation-shell .contract-meta,
                .confirmation-shell .contract-title,
                .confirmation-shell .contract-name,
                .confirmation-shell .assignment-grid,
                .confirmation-shell .clauses,
                .confirmation-shell .signature-line,
                .accepted-stamp,
                .stamp-zone::before,
                .stamp-zone::after {
                    animation: none;
                }

                .accepted-stamp {
                    opacity: 0.94;
                    transform: rotate(-7deg);
                }
            }

            @media (max-width: 760px) {
                .topbar,
                .contract-meta,
                .assignment-grid {
                    grid-template-columns: 1fr;
                }

                .topbar {
                    align-items: flex-start;
                    flex-direction: column;
                }

                .stamp-zone {
                    height: 7.5rem;
                }

                .stamp-zone::before,
                .stamp-zone::after {
                    width: 4.5rem;
                }

                .stamp-zone::before {
                    right: calc(50% + 5.6rem);
                }

                .stamp-zone::after {
                    left: calc(50% + 5.6rem);
                }
            }
        </style>
        """
    )


def render_html(markup: str) -> None:
    """Render literal HTML without letting Markdown treat indented lines as text."""
    cleaned_markup = textwrap.dedent(markup).strip()
    if hasattr(st, "html"):
        st.html(cleaned_markup)
    else:
        st.markdown(cleaned_markup, unsafe_allow_html=True)


def clean_name(full_name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z\s'-]", "", full_name).strip()
    return re.sub(r"\s+", " ", cleaned)


def deterministic_rng(full_name: str) -> random.Random:
    digest = hashlib.sha256(full_name.strip().lower().encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def generate_bathhouse_name(full_name: str) -> str:
    """Create a short new name from pieces of the submitted name."""
    cleaned = clean_name(full_name)
    rng = deterministic_rng(cleaned or "unnamed worker")

    letters = re.sub(r"[^A-Za-z]", "", cleaned).lower()
    if len(letters) >= 2:
        first_piece = letters[0].upper()
        second_piece = letters[len(letters) // 2]
        candidate = f"{first_piece}{second_piece}"
    elif letters:
        candidate = letters[0].upper()
    else:
        candidate = rng.choice(NAME_SYLLABLES)

    if rng.random() > 0.45:
        candidate += rng.choice(["n", "i", "u", "o", "a"])

    return candidate[:4]


def generate_assignment(full_name: str) -> dict:
    rng = deterministic_rng(full_name)
    role = BATHHOUSE_ROLES[rng.randrange(len(BATHHOUSE_ROLES))]
    contract_number = f"BH-{rng.randrange(1000, 9999)}-{rng.choice(['MIST', 'STEAM', 'SEAL', 'ASH'])}"
    return {
        "new_name": generate_bathhouse_name(full_name),
        "role": role["title"],
        "description": role["description"],
        "contract_number": contract_number,
    }


def reset_contract() -> None:
    for key in [
        "submitted",
        "full_name",
        "pronouns",
        "signature",
        "assignment",
    ]:
        st.session_state.pop(key, None)


def render_sidebar() -> None:
    with st.sidebar:
        st.header("About This Project")
        st.write(
            "A creative final project about contracts, identity, labor, and "
            "spectatorship in *Spirited Away*. The app uses an original fictional "
            "contract to explore how names and work are transformed by institutions."
        )


def render_header() -> None:
    status_text = "Signature Accepted" if st.session_state.get("submitted") else "Awaiting Signature"

    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand">
                <span class="brand-mark">印</span>
                <span>Bathhouse Records Office</span>
            </div>
            <span class="status-pill">{status_text}</span>
        </div>
        <section class="hero">
            <h1>Bathhouse Employment Contract</h1>
            <p>Before entering, all seekers of employment must sign.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_contract_form() -> None:
    assignment_preview = generate_assignment("prospective worker")

    st.markdown(
        f"""
        <div class="document-shell">
          <div class="document-inner">
            <div class="contract-meta">
              <div class="meta-box"><strong>Contract No.</strong>{assignment_preview["contract_number"]}</div>
              <div class="meta-box"><strong>Prepared By</strong>Bathhouse Records Office</div>
              <div class="meta-box"><strong>Status</strong>Unsigned</div>
            </div>
            <div class="contract-title">
              <h2>Terms of Service and Employment</h2>
            </div>
            <div class="clauses">
              <div class="clause">The applicant requests entry into the bathhouse as a worker and accepts that ordinary guest privileges end at the threshold.</div>
              <div class="clause">The applicant acknowledges that names carry memory, history, and obligation. Upon acceptance, the Records Office may archive the applicant's old name and issue a shorter working name.</div>
              <div class="clause">The applicant agrees to perform assigned duties with care, discretion, and respect for guests whose shapes, smells, and complaints may change without notice.</div>
              <div class="clause">The bathhouse may revise schedules during storms, feasts, inspections, or supernatural emergencies. Breaks are subject to steam pressure and ledger approval.</div>
              <div class="clause">The applicant understands that this contract is fictional and created for classroom interpretation, not for real employment, debt, or legal surrender.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("contract_form", clear_on_submit=False):
        st.subheader("Applicant Information")
        full_name = st.text_input("Full legal name", value=st.session_state.get("full_name", ""))
        pronouns = st.text_input(
            "Pronouns (optional)",
            value=st.session_state.get("pronouns", ""),
            placeholder="she/her, they/them, he/him, etc.",
        )
        agreement = st.checkbox(
            "I agree to surrender my name to the bathhouse records office and begin work under my assigned bathhouse name."
        )
        signature = st.text_input(
            "Typed signature",
            value=st.session_state.get("signature", ""),
            placeholder="Type your name as your signature",
        )

        submitted = st.form_submit_button("Sign and Surrender Name")

    if submitted:
        if not clean_name(full_name):
            st.error("Please enter a name before signing.")
        elif not agreement:
            st.error("The bathhouse cannot process unsigned surrender paperwork.")
        elif signature.strip().lower() != full_name.strip().lower():
            st.error("Your typed signature must match the submitted full name.")
        else:
            st.session_state.full_name = clean_name(full_name)
            st.session_state.pronouns = pronouns.strip()
            st.session_state.signature = signature.strip()
            st.session_state.assignment = generate_assignment(full_name)
            st.session_state.submitted = True
            st.rerun()

    st.markdown(
        '<p class="footer-note">Steam rises. Ink dries. The line continues moving.</p>',
        unsafe_allow_html=True,
    )


def render_confirmation() -> None:
    full_name = st.session_state.get("full_name", "Unnamed Worker")
    pronouns = st.session_state.get("pronouns")
    signature = st.session_state.get("signature", full_name)
    assignment = st.session_state.get("assignment", generate_assignment(full_name))
    signed_at = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    safe_full_name = html.escape(full_name)
    safe_signature = html.escape(signature)
    safe_pronouns = html.escape(pronouns) if pronouns else ""
    safe_contract_number = html.escape(assignment["contract_number"])
    safe_new_name = html.escape(assignment["new_name"])
    safe_role = html.escape(assignment["role"])
    safe_description = html.escape(assignment["description"])

    pronoun_line = f"<div class='meta-box'><strong>Pronouns</strong>{safe_pronouns}</div>" if pronouns else ""

    render_html(
        f"""
        <div class="document-shell confirmation-shell">
          <div class="document-inner">
            <div class="contract-meta">
              <div class="meta-box"><strong>Contract No.</strong>{safe_contract_number}</div>
              <div class="meta-box"><strong>Accepted</strong>{signed_at}</div>
              {pronoun_line}
            </div>
            <div class="stamp-zone" aria-label="Accepted stamp animation">
              <div class="accepted-stamp">Accepted</div>
            </div>
            <div class="contract-title">
              <h2>Your old name belongs to me now</h2>
            </div>
            <div class="contract-name">
                <h2> From now on your name is {safe_new_name}</h2>
            </div>
            <div class="assignment-grid">
              <div class="assignment-box">
                <span>Issued Bathhouse Name</span>
                <strong>{safe_new_name}</strong>
              </div>
              <div class="assignment-box">
                <span>Assigned Role</span>
                <strong>{safe_role}</strong>
              </div>
            </div>
            <div class="clauses">
              <div class="clause">First duties: {safe_description}</div>
              <div class="clause">Report to the service corridor before the next bell. Bring comfortable shoes and a willingness to be renamed by paperwork.</div>
            </div>
            <div class="signature-line">Bathhouse Records Office Seal</div>
          </div>
        </div>
        """
    )

    st.button("Reset and Sign Again", on_click=reset_contract)


def main() -> None:
    inject_css()
    render_sidebar()
    render_header()

    left, center, right = st.columns([0.08, 0.84, 0.08])
    with center:
        if st.session_state.get("submitted"):
            render_confirmation()
        else:
            render_contract_form()


if __name__ == "__main__":
    main()
