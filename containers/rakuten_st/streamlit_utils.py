import streamlit as st

PAGE_SEQUENCE = [
    {"name": "1. Home", "path": "pages/1_Home.py"},
    {"name": "2. Team Presentation", "path": "pages/2_Team_Presentation.py"},
    {"name": "3. Key Focus Areas", "path": "pages/3_Key_Focus_Areas.py"},
    {"name": "4. Flowcharts", "path": "pages/4_Flowcharts.py"},
    {"name": "10. tmp", "path": "pages/10_tmp.py"}
]

def add_pagination_and_footer(current_page_path):
    # Find current page index in sequence
    current_index = next(
        (
            i
            for i, page in enumerate(PAGE_SEQUENCE)
            if page["path"] == current_page_path
        ),
        0,
    )

    # Create columns for previous, current page indicator, next
    prev_butt, next_butt = st.columns(
        2
    )  # elf* and erc* as in "empty left column" and "empty right column"

    # Previous button
    with prev_butt:
        if current_index > 0:  # Not on first page
            prev_page = PAGE_SEQUENCE[current_index - 1]
            if st.button("← Previous", use_container_width=True):
                st.switch_page(prev_page["path"])

    # Next button
    with next_butt:
        if current_index < len(PAGE_SEQUENCE) - 1:  # Not on last page
            next_page = PAGE_SEQUENCE[current_index + 1]
            if st.button("Next →", use_container_width=True):
                st.switch_page(next_page["path"])

    # Copyright line and page indicator
    st.markdown(
        f"© 2025 // Marie Ernø-Møller, Peter Stieg, Qi Bao, Robert Wilson // [Page {current_index + 1}/{len(PAGE_SEQUENCE)}]"
    )

def hw():
    """Test function to print "Hello, world!".

    This function serves as a placeholder to demonstrate the module's structure.
    """
    print("Hello, world!")