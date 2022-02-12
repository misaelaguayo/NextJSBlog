describe("Main Page", () => {
  it("Should show the linked in link", () => {
    cy.visit("http://localhost:3000/");

    cy.get('a[href*="linkedin"]');
  });
});
