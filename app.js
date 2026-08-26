const authorisedDays = 56;
const unauthorisedDays = 395;

function daysBetween(start, end) {
  const ms = Date.parse(end) - Date.parse(start);
  return Math.floor(ms / 86400000);
}

function assess(data) {
  const days = daysBetween(data.debitDate, data.assessmentDate);
  const missing = [];
  const warnings = [];
  if (!data.mandate) missing.push('mandate/reference or authorisation record');
  if (!data.notice) missing.push('prior notice or invoice');
  if (days < 0) warnings.push('assessment date is before debit date');

  let route = 'authorisation unknown';
  let window = 'outside standard windows';
  let action = 'Ask the bank for written options; standard windows may be exceeded.';

  if (data.status === 'unauthorized') {
    route = 'unauthorised direct debit';
    if (days >= 0 && days <= unauthorisedDays) {
      window = 'inside the thirteen-month unauthorised claim route';
      action = 'Ask the bank to refund an unauthorised direct debit and provide mandate evidence if requested.';
    } else {
      window = 'outside the thirteen-month unauthorised claim route';
      warnings.push('standard unauthorised window exceeded');
    }
  } else if (data.status === 'authorized') {
    route = 'authorised direct debit';
    if (days >= 0 && days <= authorisedDays) {
      window = 'inside the eight-week no-questions refund window';
      action = 'Ask the bank for the standard authorised SEPA Direct Debit refund within eight weeks.';
    } else {
      window = 'outside the standard authorised refund window';
      action = 'Ask the bank or creditor for written options; the ordinary eight-week authorised refund window appears exceeded.';
      warnings.push('authorised eight-week window may be exceeded');
    }
  } else if (days >= 0 && days <= authorisedDays) {
    window = 'inside eight weeks if authorised, and inside thirteen months if unauthorised';
    action = 'Ask the bank to classify the debit and preserve both authorised and unauthorised refund arguments.';
  } else if (days >= 0 && days <= unauthorisedDays) {
    window = 'outside eight weeks but inside thirteen months if unauthorised';
    action = 'Request mandate evidence; if no valid mandate exists, ask about the unauthorised direct debit refund route.';
    warnings.push('authorised eight-week window may be exceeded');
  }

  return {days, route, window, action, missing, warnings};
}

function draft(data, assessment) {
  return `To: ${data.bank}\nSubject: SEPA Direct Debit refund request for ${data.creditor}\n\nPlease review the SEPA Direct Debit collected by ${data.creditor} on ${data.debitDate} for ${Number(data.amount).toFixed(2)} EUR.\n\nCurrent classification: ${assessment.route}; timing: ${assessment.window} (${assessment.days} days since debit).\n\nRequested action: ${assessment.action}\n\nEvidence to check or attach: bank statement, mandate/reference, creditor notice or invoice, and communication with the creditor. Missing or uncertain evidence flagged by this draft: ${assessment.missing.join(', ') || 'none currently flagged'}.\n\nThis is an editable draft based on general public information. Please verify applicable scheme, local banking rules and deadlines before sending.\n`;
}

document.getElementById('sepa-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const data = {
    bank: document.getElementById('bank').value,
    creditor: document.getElementById('creditor').value,
    amount: document.getElementById('amount').value,
    debitDate: document.getElementById('debitDate').value,
    assessmentDate: document.getElementById('assessmentDate').value,
    status: document.getElementById('status').value,
    mandate: document.getElementById('mandate').checked,
    notice: document.getElementById('notice').checked,
  };
  const assessment = assess(data);
  document.getElementById('result').textContent = JSON.stringify({
    route: assessment.route,
    likely_window: assessment.window,
    days_since_debit: assessment.days,
    suggested_action: assessment.action,
    missing_evidence: assessment.missing,
    warnings: assessment.warnings,
  }, null, 2);
  document.getElementById('draft').value = draft(data, assessment);
});

document.getElementById('sepa-form').dispatchEvent(new Event('submit'));
