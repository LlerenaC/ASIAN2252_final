import hashlib
import random
import re
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
    st.markdown(
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
                font-size: clamp(2.2rem, 6vw, 4.75rem);
                line-height: 0.95;
                margin: 0 0 0.75rem;
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
                border-bottom: 2px solid rgba(36, 25, 21, 0.55);
                padding: 0.85rem 0;
                margin-bottom: 1.15rem;
                text-align: center;
            }

            .contract-title h2 {
                margin: 0;
                font-size: clamp(1.45rem, 4vw, 2.25rem);
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

            .accepted-stamp {
                display: inline-block;
                transform: rotate(-7deg);
                border: 0.24rem solid var(--seal);
                color: var(--seal);
                padding: 0.35rem 0.85rem;
                margin: 0.25rem 0 1rem;
                font-size: clamp(2rem, 6vw, 4rem);
                font-weight: 900;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                opacity: 0.92;
                mix-blend-mode: multiply;
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
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
        st.divider()
        st.caption(
            "No copyrighted film stills, official logos, or quoted dialogue are used. "
            "The visual language is inspired by digital signing tools and Japanese "
            "bathhouse motifs without copying protected assets."
        )


def render_header() -> None:
    st.markdown(
        """
        <div class="topbar">
            <div class="brand">
                <span class="brand-mark">印</span>
                <span>Bathhouse Records Office</span>
            </div>
            <span class="status-pill">Awaiting Signature</span>
        </div>
        <section class="hero">
            <h1>Bathhouse Employment Contract</h1>
            <p>Before entering, all guests must sign.</p>
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
              <h2>Fictional Terms of Service and Employment</h2>
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

    pronoun_line = f"<div class='meta-box'><strong>Pronouns</strong>{pronouns}</div>" if pronouns else ""

    st.markdown(
        f"""
        <div class="document-shell">
          <div class="document-inner">
            <div class="contract-meta">
              <div class="meta-box"><strong>Contract No.</strong>{assignment["contract_number"]}</div>
              <div class="meta-box"><strong>Accepted</strong>{signed_at}</div>
              {pronoun_line}
            </div>
            <div class="accepted-stamp">Accepted</div>
            <div class="contract-title">
              <h2>Your old name has been archived.</h2>
            </div>
            <div class="assignment-grid">
              <div class="assignment-box">
                <span>Issued Bathhouse Name</span>
                <strong>{assignment["new_name"]}</strong>
              </div>
              <div class="assignment-box">
                <span>Assigned Role</span>
                <strong>{assignment["role"]}</strong>
              </div>
            </div>
            <div class="clauses">
              <div class="clause">Former name on file: {full_name}</div>
              <div class="clause">Signature received: {signature}</div>
              <div class="clause">First duties: {assignment["description"]}</div>
              <div class="clause">Report to the service corridor before the next bell. Bring comfortable shoes and a willingness to be renamed by paperwork.</div>
            </div>
            <div class="signature-line">Bathhouse Records Office Seal</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
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
